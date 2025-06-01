# Video Folder Cleaner

**Version:** 1.0.0

## Overview

Video Folder Cleaner is a user-friendly desktop application designed to help you organize and clean up your video collections efficiently. It scans a selected root folder containing multiple subfolders, identifies video files, and automates the management of video formats based on your preferences.

## Key Features

- **Scan Subfolders:** Quickly scans each subfolder for video files with popular formats like MP4, MOV, MKV, AVI, and more.
- **MP4 Verification:** Detects whether a matching `.mp4` file exists for each folder based on folder name.
- **Customizable Format Management:** Choose which video formats to keep or delete via an intuitive menu.
- **Backup Option:** Optionally back up deleted files to a designated folder before removal.
- **Automated Cleanup:** Moves folders missing MP4 files to a separate `no_mp4` folder and deletes unwanted formats automatically.
- **Drag & Drop Support:** Easily select your root folder by dragging it into the application window.
- **Progress Tracking:** Visual progress bar shows cleanup progress.
- **Log File Generation:** Keeps a detailed log of all actions for transparency and troubleshooting.
- **Portable Executable:** Runs as a standalone `.exe` with no installation required, customizable with your icon and version info.

## Usage

1. Launch the program.
2. Select the root folder containing your video subfolders (or drag & drop it).
3. Choose the video formats you want to delete or keep.
4. Toggle backup on/off if desired.
5. Click **Run Automated Cleanup** to start.
6. Review the log and updated folder structure after completion.

## Requirements

- Windows OS
- No installation needed — portable executable
- Python included in the build (if running from source)

## License

GNU General Public License v3.0

---

Made with ❤️ for easy and efficient video folder management.
