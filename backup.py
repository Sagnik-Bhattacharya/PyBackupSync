import os, shutil, hashlib, json
from datetime import datetime
from zipfile import ZipFile

BACKUP_DIR = "backups"
HASH_FILE = "last_backup.json"

def hash_file(path):
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_last_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f)

def backup_folder(source, zip_backup=False, progress_callback=None):
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source folder '{source}' not found.")

    os.makedirs(BACKUP_DIR, exist_ok=True)

    # Get all files to backup
    all_files = []
    for root, _, files in os.walk(source):
        for file in files:
            all_files.append(os.path.join(root, file))
    total_files = len(all_files)

    last_hashes = load_last_hashes()
    current_hashes = {}

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dest_folder = os.path.join(BACKUP_DIR, timestamp)
    os.makedirs(dest_folder)

    copied_files = 0

    for src_path in all_files:
        rel_path = os.path.relpath(src_path, source)
        file_hash = hash_file(src_path)
        current_hashes[rel_path] = file_hash

        if rel_path not in last_hashes or last_hashes[rel_path] != file_hash:
            dest_path = os.path.join(dest_folder, rel_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)

        copied_files += 1
        if progress_callback:
            progress_callback(copied_files, total_files, rel_path)

    save_hashes(current_hashes)

    if zip_backup:
        zip_path = f"{dest_folder}.zip"
        with ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(dest_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, dest_folder)
                    zipf.write(file_path, arcname)
        shutil.rmtree(dest_folder)  # remove folder after zipping
        return f"Backup created & zipped: {zip_path}"
    else:
        return f"Backup created: {dest_folder}"
