import os
import sys
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# Auto-install tkinterdnd2 if missing
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinterdnd2"])
    from tkinterdnd2 import DND_FILES, TkinterDnD

LOG_FILE = "cleanup_log.txt"
COMMON_FORMATS = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv', '.ogv', '.3gp', '.mpeg']

def write_log(message):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(message + "\n")

class VideoCleanerApp:
    def __init__(self, master):
        self.master = master
        master.title("Video Folder Cleaner")

        self.root_folder = ""
        self.results = []
        self.format_vars = {ext: tk.IntVar(value=1 if ext == '.mp4' else 0) for ext in COMMON_FORMATS}
        self.backup_var = tk.BooleanVar(value=True)

        # Folder selection
        tk.Label(master, text="Drag a folder here or click to browse:").pack(pady=(10, 0))
        self.drop_area = tk.Label(master, text="📂 Drop folder here", bg="#f0f0f0", width=50, height=3, relief="ridge")
        self.drop_area.pack(pady=5)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)
        tk.Button(master, text="Browse Folder", command=self.browse_folder).pack()

        # Backup toggle
        tk.Checkbutton(master, text="Backup deleted files", variable=self.backup_var).pack(pady=5)

        # Format selection checkboxes
        fmt_frame = tk.LabelFrame(master, text="Select formats to KEEP", padx=10, pady=5)
        fmt_frame.pack(padx=10, pady=5)
        for i, ext in enumerate(COMMON_FORMATS):
            tk.Checkbutton(fmt_frame, text=ext, variable=self.format_vars[ext]).grid(row=i//5, column=i%5, sticky='w')

        # Progress bar and action
        self.progress = ttk.Progressbar(master, mode='determinate', length=400)
        self.progress.pack(pady=10)
        tk.Button(master, text="Run Automated Cleanup", command=self.run_automated).pack(pady=5)

        # Result table
        self.tree = ttk.Treeview(master, columns=('Subfolder', 'MP4 Available', 'Other Formats'), show='headings')
        self.tree.heading('Subfolder', text='Subfolder')
        self.tree.heading('MP4 Available', text='MP4 Available')
        self.tree.heading('Other Formats', text='Other Formats')
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

    def get_keep_extensions(self):
        return {ext for ext, var in self.format_vars.items() if var.get() == 1}

    def get_delete_extensions(self):
        return {ext for ext, var in self.format_vars.items() if var.get() == 0}

    def on_drop(self, event):
        path = event.data.strip().strip("{").strip("}")
        if os.path.isdir(path):
            self.root_folder = path
            self.scan_and_display()

    def browse_folder(self):
        self.root_folder = filedialog.askdirectory()
        if self.root_folder:
            self.scan_and_display()

    def scan_and_display(self):
        self.results = self.scan_videos(self.root_folder)
        self.populate_tree()

    def scan_videos(self, root_folder):
        results = []
        for subdir in next(os.walk(root_folder))[1]:
            subdir_path = os.path.join(root_folder, subdir)
            files = [f for f in os.listdir(subdir_path)
                     if os.path.isfile(os.path.join(subdir_path, f))
                     and os.path.splitext(f)[1].lower() in COMMON_FORMATS]
            base_matches = [f for f in files if os.path.splitext(f)[0] == subdir]
            mp4_found = any(f.lower().endswith('.mp4') for f in base_matches)

            results.append({
                'Subfolder': subdir,
                'Path': subdir_path,
                'MP4 Available': mp4_found,
                'Matching Videos': base_matches,
                'Other Formats': ', '.join([os.path.splitext(f)[1] for f in base_matches if not f.lower().endswith('.mp4')]),
            })
        return results

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for r in self.results:
            self.tree.insert('', 'end',
                values=(r['Subfolder'], 'Yes' if r['MP4 Available'] else 'No', r['Other Formats']))

    def run_automated(self):
        if not self.root_folder:
            messagebox.showerror("Error", "No folder selected.")
            return

        keep_exts = self.get_keep_extensions()
        delete_exts = self.get_delete_extensions()

        self.results = self.scan_videos(self.root_folder)
        total = len(self.results)
        self.progress['maximum'] = total
        self.progress['value'] = 0
        self.master.update_idletasks()

        parent = os.path.dirname(self.root_folder)
        no_mp4_dir = os.path.join(parent, 'no_mp4')
        backup_dir = os.path.join(parent, 'backup_deleted') if self.backup_var.get() else None

        os.makedirs(no_mp4_dir, exist_ok=True)
        if backup_dir:
            os.makedirs(backup_dir, exist_ok=True)

        moved = deleted = 0
        write_log("=== Cleanup Started ===")
        write_log(f"Root folder: {self.root_folder}")
        write_log(f"Keep: {keep_exts}")
        write_log(f"Delete: {delete_exts}")
        write_log(f"Backup: {bool(backup_dir)}\n")

        for i, res in enumerate(self.results):
            folder = res['Subfolder']
            path = res['Path']

            if not res['MP4 Available']:
                dest = os.path.join(no_mp4_dir, folder)
                if not os.path.exists(dest):
                    shutil.move(path, dest)
                    moved += 1
                    write_log(f"Moved: {folder}")
            else:
                for f in res['Matching Videos']:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in delete_exts:
                        full_path = os.path.join(path, f)
                        try:
                            if backup_dir:
                                dest = os.path.join(backup_dir, folder)
                                os.makedirs(dest, exist_ok=True)
                                shutil.copy2(full_path, os.path.join(dest, f))
                            os.remove(full_path)
                            deleted += 1
                            write_log(f"Deleted: {f} from {folder}")
                        except Exception as e:
                            write_log(f"Error deleting {f}: {e}")
            self.progress['value'] = i + 1
            self.master.update_idletasks()

        write_log(f"\nMoved {moved} folder(s). Deleted {deleted} file(s).")
        write_log("=== Cleanup Complete ===\n")
        self.scan_and_display()
        messagebox.showinfo("Done", f"Moved {moved} folders.\nDeleted {deleted} files.\nSee log in {LOG_FILE}")

if __name__ == "__main__":
    try:
        root = TkinterDnD.Tk()
    except Exception:
        root = tk.Tk()

    app = VideoCleanerApp(root)
    root.geometry("760x620")
    root.mainloop()
