# 🗄 PyBackupSync - Premium Edition

A powerful, premium-looking **desktop application** built with **CustomTkinter** for **backup, restore, encryption, and decryption** of files and folders — all with a sleek, modern UI and progress feedback.

---

## Features

- **Backup** entire folders with incremental file copying and progress bar
- **Restore** backups to any destination folder safely
- **Encrypt** and **Decrypt** files using secure symmetric encryption (Fernet)
- Multi-threaded operations to keep UI responsive
- Detailed **progress bar** and **log console** for real-time status updates
- Premium, dark-themed UI using CustomTkinter
- Prevents accidental overwriting/restoration in the backup directory
- Supports large folder backups with hashing to avoid redundant copies

---

## Screenshots

*(Add screenshots here to show the UI, progress bar, and logs)*

---

## Installation

### Prerequisites

- Python 3.8+
- CustomTkinter (for modern themed UI)
- cryptography (for encryption/decryption)

### Install dependencies

```bash
pip install customtkinter cryptography
````

---

## Usage

### Run the application

```bash
python ui.py
```

### Workflow

1. **Select Source Folder/File:** Use "Browse" buttons to select source files/folders
2. **Select Destination Folder:** For restoring backups or saving encrypted files
3. **Choose action:** Click Backup, Restore, Encrypt, or Decrypt buttons
4. **Monitor progress:** Progress bar and log console show real-time updates

---

## Project Structure

```
PyBackupSync/
│
├── ui.py                # Main CustomTkinter GUI app
├── main.py              # Core logic: key generation, encrypt/decrypt helpers
├── backup.py            # Backup logic with incremental backup & progress callback
├── restore.py           # Restore logic to copy backup to destination
├── backups/             # Backup folders created here (do not commit this!)
├── secret.key           # Encryption key file (auto-generated)
├── README.md            # This file
├── backup.log           # Log file for operations
└── last_backup.json     # Hashes of last backup for incremental backup
```

---

## Development Notes

* Backups are incremental and use file hashes to avoid re-copying unchanged files.
* Progress is reported via a callback function updating the GUI progress bar and log.
* Encryption uses Fernet symmetric key encryption with a persistent key stored in `secret.key`.
* Restoring prevents overwriting inside the backups folder to avoid data corruption.
* The app uses threads for running long tasks without freezing the UI.
* Make sure to **never commit your `backups/` folder or `secret.key`** to version control.

---

## Troubleshooting

* **Git warnings about CRLF:** These are normal on Windows and related to line endings. No action needed.
* **Nested Git repositories:** Avoid initializing Git repos inside your `backups/` folder or other project subfolders.
* **Backup or restore errors:** Check folder paths and permissions. Logs will be saved in `backup.log`.
* **Encryption errors:** Ensure files exist and have correct permissions.

---


## Contact

Created by Sagnik Bhattacharya
---

*Thank you for using PyBackupSync!*
