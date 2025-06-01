# Video Folder Cleaner

**Version:** 1.0.0

---

## 🎞️ Overview

**Video Folder Cleaner** is a user-friendly, standalone desktop application that scans video folders, detects whether a correctly named `.mp4` file exists, and lets you automatically remove or back up other video formats. It’s ideal for video collectors, archivists, or anyone cleaning large video libraries.

---

## ✅ Features

* 🔍 **Scan subfolders** for videos named after the folder.
* 🎯 **Check for `.mp4` availability** per folder.
* ⚙️ **Select formats** to delete or keep via checkboxes.
* 💾 **Backup option** for deleted files.
* 📂 **Drag & drop support** for selecting folders.
* 📊 **Progress bar** for automation steps.
* 📜 **Log file output** to `cleaner_log.txt`.
* 📦 **Single portable executable** (no install required).
* 🖼️ **Custom icon** and version metadata embedded in `.exe`.

---

## 🛍️ How to Use

1. **Launch the app** (run `VideoFolderCleaner.exe` or from Python).
2. Click **Browse** or drag a folder into the window.
3. Choose which formats to **delete** and **keep**.
4. (Optional) Enable **Backup Deleted Files**.
5. Click **Run Automated Cleanup**.
6. Done! See `cleaner_log.txt` for operation history.

---

## 🏗️ Build Guide

You can build your own portable `.exe` using the provided PowerShell script.

### ⚖️ Requirements

* Windows
* Python 3.10 or newer
* `pip` (comes with Python)
* PowerShell 5+

---

### 📂 Project Structure Example

```
/project-folder/
│
├── main.py                 ← Your main Python script
├── build.ps1               ← Build script (PowerShell)
└── icon.ico                ← App icon

```

---

### ▶️ One-Liner Build Command (PowerShell)

To run the build script, open a PowerShell window in the project folder and paste:

```powershell
Set-ExecutionPolicy -Scope Process Bypass; .\build.ps1
```

> ℹ️ The script will install required dependencies and build the `.exe`.

---

### 🧪 What `build.ps1` Does

* Installs **PyInstaller** and other dependencies (if needed).
* Uses `pyinstaller` to create a **standalone executable**.
* Embeds:

  * `icon.ico` as the app icon.
  * Version metadata (Product name, Company, File version).
* Outputs:

  * `dist/VideoFolderCleaner.exe`
  * Logfile: `cleaner_log.txt`

---

## 📁 Output

After building, you’ll find your finished `.exe` in the `dist/` directory, ready to share or run on any Windows machine without installation.

---

## 📄 License

This project is licensed under the GPT3 License. Feel free to use and modify it.

---
