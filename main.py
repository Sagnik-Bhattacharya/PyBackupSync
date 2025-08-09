import argparse
import os
import shutil
import logging
from datetime import datetime
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(
    filename="backup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Generate or load encryption key
KEY_FILE = "secret.key"

def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        logging.info("New encryption key generated.")
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

def backup(source_folder):
    if not os.path.exists(source_folder):
        logging.error(f"Source folder '{source_folder}' does not exist.")
        print(f"❌ Source folder not found: {source_folder}")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join("backups", f"backup_{timestamp}")

    os.makedirs(backup_folder, exist_ok=True)
    try:
        shutil.copytree(source_folder, backup_folder, dirs_exist_ok=True)
        logging.info(f"Backup completed from '{source_folder}' to '{backup_folder}'.")
        print(f"✅ Backup completed: {backup_folder}")
    except Exception as e:
        logging.error(f"Backup failed: {e}")
        print(f"❌ Backup failed: {e}")

def restore(backup_folder, destination_folder):
    if not os.path.exists(backup_folder):
        logging.error(f"Backup folder '{backup_folder}' does not exist.")
        print(f"❌ Backup folder not found: {backup_folder}")
        return

    try:
        shutil.copytree(backup_folder, destination_folder, dirs_exist_ok=True)
        logging.info(f"Restore completed from '{backup_folder}' to '{destination_folder}'.")
        print(f"✅ Restore completed to: {destination_folder}")
    except Exception as e:
        logging.error(f"Restore failed: {e}")
        print(f"❌ Restore failed: {e}")

def encrypt_file(file_path, fernet):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        encrypted_data = fernet.encrypt(data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        return f"Encrypted: {file_path}"
    except Exception as e:
        raise RuntimeError(f"Encryption failed for {file_path}: {e}")

def decrypt_file(file_path, fernet):
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        decrypted_data = fernet.decrypt(data)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        logging.info(f"File decrypted: {file_path}")
        print(f"🔓 Decrypted: {file_path}")
    except Exception as e:
        logging.error(f"Decryption failed for {file_path}: {e}")
        print(f"❌ Decryption failed for {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cryptex - Backup & Encryption Tool")
    parser.add_argument("command", choices=["backup", "restore", "encrypt", "decrypt"], help="Command to run")
    parser.add_argument("source", help="Source folder or file path")
    parser.add_argument("destination", nargs="?", help="Destination folder (only for restore)")

    args = parser.parse_args()
    fernet = load_or_create_key()

    if args.command == "backup":
        backup(args.source)
    elif args.command == "restore":
        if not args.destination:
            print("❌ Destination folder required for restore.")
        else:
            restore(args.source, args.destination)
    elif args.command == "encrypt":
        encrypt_file(args.source, fernet)
    elif args.command == "decrypt":
        decrypt_file(args.source, fernet)
