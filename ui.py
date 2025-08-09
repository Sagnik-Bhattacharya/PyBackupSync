import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os

# Import your logic files
import main as cryptex
import backup as backup_module
import restore as restore_module

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class PyBackupSyncApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PyBackupSync - Premium Edition")
        self.geometry("950x650")
        self.configure(fg_color="#121212")

        # --- Title ---
        title = ctk.CTkLabel(self, text="🗄 PyBackupSync", font=("Segoe UI", 36, "bold"))
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(self, text="Backup • Restore • Encrypt • Decrypt", font=("Segoe UI", 16))
        subtitle.pack(pady=(0, 20))

        # --- Frame ---
        self.frame = ctk.CTkFrame(self, corner_radius=15, fg_color=("gray10", "gray20"))
        self.frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Source Entry
        self.src_entry = ctk.CTkEntry(self.frame, placeholder_text="Select Source Folder / File")
        self.src_entry.pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(self.frame, text="Browse", command=self.select_source).pack()

        # Destination Entry
        self.dest_entry = ctk.CTkEntry(self.frame, placeholder_text="Select Destination Folder")
        self.dest_entry.pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(self.frame, text="Browse", command=self.select_destination).pack()
        
        self.progress_bar = ctk.CTkProgressBar(self.frame)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Add inside your __init__, below the Destination Entry:

# Label for backups list
        self.backups_label = ctk.CTkLabel(self.frame, text="Available Backups:", font=("Segoe UI", 14))
        self.backups_label.pack(pady=(10, 5), padx=20, anchor="w")

        # Listbox or CTkComboBox to list backup folders
        self.backups_listbox = ctk.CTkComboBox(self.frame, values=[])
        self.backups_listbox.pack(fill="x", padx=20)
        self.backups_listbox.bind("<<ComboboxSelected>>", self.backup_selected)

        # Button to refresh backups list
        refresh_btn = ctk.CTkButton(self.frame, text="🔄 Refresh Backups", command=self.load_backups)
        refresh_btn.pack(pady=(5,15))

        # Call load_backups at startup to populate the list
        self.load_backups()



        # --- Buttons Row ---
        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="🚀 Backup", fg_color="#00b894", hover_color="#00cec9",
                      command=self.start_backup).grid(row=0, column=0, padx=10)

        ctk.CTkButton(btn_frame, text="📥 Restore", fg_color="#0984e3", hover_color="#74b9ff",
                      command=self.start_restore).grid(row=0, column=1, padx=10)

        ctk.CTkButton(btn_frame, text="🔒 Encrypt", fg_color="#d63031", hover_color="#ff7675",
                      command=self.start_encrypt).grid(row=0, column=2, padx=10)

        ctk.CTkButton(btn_frame, text="🔓 Decrypt", fg_color="#6c5ce7", hover_color="#a29bfe",
                      command=self.start_decrypt).grid(row=0, column=3, padx=10)

        # --- Log Console ---
        self.log_text = ctk.CTkTextbox(self.frame, height=200)
        self.log_text.pack(pady=15, fill="both", padx=20)

    # === UI Helpers ===
    def select_source(self):
        path = filedialog.askdirectory()
        if path:
            self.src_entry.delete(0, ctk.END)
            self.src_entry.insert(0, path)

    def select_destination(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_entry.delete(0, ctk.END)
            self.dest_entry.insert(0, path)

    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def run_in_thread(self, func, *args):
        threading.Thread(target=func, args=args, daemon=True).start()

    # === Functional Buttons ===
    def start_backup(self):
        src = self.src_entry.get()
        if not src:
            messagebox.showerror("Error", "Please select a source folder.")
            return
        self.run_in_thread(self.backup_process, src)

    def start_restore(self):
        backup_folder = self.src_entry.get()
        dest = self.dest_entry.get()
        if not backup_folder or not dest:
            messagebox.showerror("Error", "Please select both backup folder and destination.")
            return
        self.run_in_thread(self.restore_process, backup_folder, dest)

    def start_encrypt(self):
        file_path = self.src_entry.get()
        if not file_path or not os.path.isfile(file_path):
            messagebox.showerror("Error", "Please select a valid file to encrypt.")
            return
        self.run_in_thread(self.encrypt_process, file_path)

    def start_decrypt(self):
        file_path = self.src_entry.get()
        if not file_path or not os.path.isfile(file_path):
            messagebox.showerror("Error", "Please select a valid file to decrypt.")
            return
        self.run_in_thread(self.decrypt_process, file_path)

    # === Backend Integration ===
    def backup_process(self, src):
        def progress_callback(copied_files, total_files, current_file):
            progress = copied_files / total_files
            self.after(0, lambda: [
                self.log(f"⏳ Backing up ({copied_files}/{total_files}): {current_file}"),
                self.progress_bar.set(progress)
            ])

        self.log(f"🔄 Starting backup from {src}...")
        try:
            msg = backup_module.backup_folder(src, progress_callback=progress_callback)
            self.log(f"✅ {msg}")
        except Exception as e:
            self.log(f"❌ Backup failed: {e}")

    def restore_process(self, backup_folder, dest):
        self.log(f"📥 Restoring {backup_folder} to {dest}...")
        try:
            # Extract backup folder name relative to backups directory
            backup_name = os.path.basename(backup_folder.rstrip(os.sep))
            msg = restore_module.restore_folder(backup_name, dest)
            self.log(f"✅ {msg}")
        except Exception as e:
            self.log(f"❌ Restore failed: {e}")


    def encrypt_process(self, file_path):
        self.log(f"🔒 Encrypting file: {file_path}...")
        try:
            fernet = cryptex.load_or_create_key()
            cryptex.encrypt_file(file_path, fernet)
            self.log("✅ File encrypted.")
        except Exception as e:
            self.log(f"❌ Encryption failed: {e}")

    def decrypt_process(self, file_path):
        self.log(f"🔓 Decrypting file: {file_path}...")
        try:
            fernet = cryptex.load_or_create_key()
            cryptex.decrypt_file(file_path, fernet)
            self.log("✅ File decrypted.")
        except Exception as e:
            self.log(f"❌ Decryption failed: {e}")

    def progress_callback(self,copied_files, total_files, current_file):
        progress_percent = (copied_files / total_files) * 100
        message = f"⏳ Backing up ({copied_files}/{total_files}) : {current_file} ({progress_percent:.1f}%)"
        self.after(0, lambda: self.log(message))
    
    def load_backups(self):
        backups_path = "backups"
        if not os.path.exists(backups_path):
            os.makedirs(backups_path)
        backups = [f for f in os.listdir(backups_path) if os.path.isdir(os.path.join(backups_path, f))]
        backups.sort(reverse=True)  # recent first
        self.backups_listbox.configure(values=backups)
        if backups:
            self.backups_listbox.set(backups[0])  # Select latest by default

    def backup_selected(self, event=None):
        selected = self.backups_listbox.get()
        if selected:
            # Pre-fill the src_entry (for restore source) with the backup folder path
            self.src_entry.delete(0, ctk.END)
            self.src_entry.insert(0, os.path.join("backups", selected))
if __name__ == "__main__":
    app = PyBackupSyncApp()
    app.mainloop()
