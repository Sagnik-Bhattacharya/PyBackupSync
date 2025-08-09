import os
import shutil
import sys
from datetime import datetime

BACKUP_DIR = "backups"

def restore_folder(backup_name, destination):
    backup_path = os.path.join("backups", backup_name)
    
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup '{backup_name}' not found in backups folder.")

    if os.path.abspath(destination).startswith(os.path.abspath("backups")):
        raise ValueError("Cannot restore into the backups directory itself!")

    file_count = 0
    for root, _, files in os.walk(backup_path):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, backup_path)
            dest_path = os.path.join(destination, rel_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            file_count += 1

    return f"Successfully restored '{backup_name}' to '{destination}' ({file_count} files)."

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python restore.py <backup_name> <destination_folder>")
        sys.exit(1)

    backup_name = sys.argv[1]
    destination = sys.argv[2]
    
    restore_folder(backup_name, destination)
