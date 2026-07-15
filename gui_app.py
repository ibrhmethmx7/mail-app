import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
import config
import backup_manager
import license_manager
import os

import threading
import config
import backup_manager
import license_manager
import os

# Translations
TRANSLATIONS = {
    "en": {
        "title": "AntArge Mail Backup",
        "settings": "Mail Settings",
        "email": "Email:",
        "password": "Password:",
        "server": "Server:",
        "options": "Options",
        "delete": "Delete emails from server after backup",
        "organize": "Organize by Date (Year/Month folders)",
        "start": "Start Backup",
        "open": "Open Backup Folder",
        "success": "Process Finished",
        "error": "Error",
        "license_check": "License Check",
        "enter_email": "Enter Email Address:",
        "enter_key": "Enter License Key:",
        "license_valid": "License Validated!",
        "license_invalid": "Invalid License Key!",
        "online_valid": "Online License Validated!",
        "online_invalid": "Invalid License (Online Check Failed)!",
        "email_required": "Email is required for license check.",
        "key_required": "License Key is required.",
        "lang_label": "Language / Dil:"
    },
    "tr": {
        "title": "AntArge Mail Yedekleme",
        "settings": "Mail Ayarları",
        "email": "E-posta:",
        "password": "Şifre:",
        "server": "Sunucu:",
        "options": "Seçenekler",
        "delete": "Yedeklemeden sonra sunucudan sil (Yer aç)",
        "organize": "Tarihe göre klasörle (Yıl/Ay)",
        "start": "Yedeklemeyi Başlat",
        "open": "Yedek Klasörünü Aç",
        "success": "İşlem Tamamlandı",
        "error": "Hata",
        "license_check": "Lisans Kontrolü",
        "enter_email": "E-posta Adresinizi Girin:",
        "enter_key": "Lisans Anahtarını Girin:",
        "license_valid": "Lisans Doğrulandı!",
        "license_invalid": "Geçersiz Lisans Anahtarı!",
        "online_valid": "Online Lisans Doğrulandı!",
        "online_invalid": "Geçersiz Lisans (Online Kontrol Başarısız)!",
        "email_required": "Lisans kontrolü için e-posta gereklidir.",
        "key_required": "Lisans anahtarı gereklidir.",
        "lang_label": "Language / Dil:"
    }
}

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "tr" # Default Turkish
        self.root.title(TRANSLATIONS[self.current_lang]["title"])
        self.root.geometry("600x650")
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # Check License
        self.check_license()

        # Main Frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Language Selection
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(lang_frame, text="Language / Dil:").pack(side=tk.LEFT)
        self.lang_combo = ttk.Combobox(lang_frame, values=["Türkçe", "English"], state="readonly", width=10)
        self.lang_combo.set("Türkçe")
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)

        # Title
        self.title_label = ttk.Label(main_frame, text=self.t("title"), font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=(0, 20))

        # Credentials Frame
        self.cred_frame = ttk.LabelFrame(main_frame, text=self.t("settings"), padding="10")
        self.cred_frame.pack(fill=tk.X, pady=5)

        # Email
        self.email_label = ttk.Label(self.cred_frame, text=self.t("email"))
        self.email_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        self.email_entry = ttk.Entry(self.cred_frame, width=30)
        self.email_entry.insert(0, config.EMAIL_USER)
        self.email_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        # Password
        self.pass_label = ttk.Label(self.cred_frame, text=self.t("password"))
        self.pass_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        self.pass_entry = ttk.Entry(self.cred_frame, width=30, show="*")
        self.pass_entry.insert(0, config.EMAIL_PASS)
        self.pass_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        # Server
        self.server_label = ttk.Label(self.cred_frame, text=self.t("server"))
        self.server_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        self.server_entry = ttk.Entry(self.cred_frame, width=30)
        self.server_entry.insert(0, config.IMAP_SERVER)
        self.server_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

        # Options Frame
        self.opt_frame = ttk.LabelFrame(main_frame, text=self.t("options"), padding="10")
        self.opt_frame.pack(fill=tk.X, pady=10)

        self.delete_var = tk.BooleanVar(value=config.DELETE_AFTER_BACKUP)
        self.delete_check = ttk.Checkbutton(self.opt_frame, text=self.t("delete"), variable=self.delete_var)
        self.delete_check.pack(anchor=tk.W)

        self.organize_var = tk.BooleanVar(value=config.ORGANIZE_BY_DATE)
        self.organize_check = ttk.Checkbutton(self.opt_frame, text=self.t("organize"), variable=self.organize_var)
        self.organize_check.pack(anchor=tk.W)

        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=10)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(main_frame, height=10, state='disabled', font=("Consolas", 10))
        self.log_area.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.start_btn = ttk.Button(btn_frame, text=self.t("start"), command=self.start_backup_thread)
        self.start_btn.pack(side=tk.RIGHT, padx=5)

        self.open_btn = ttk.Button(btn_frame, text=self.t("open"), command=self.open_folder)
        self.open_btn.pack(side=tk.LEFT, padx=5)

    def t(self, key):
        return TRANSLATIONS[self.current_lang].get(key, key)

    def change_language(self, event=None):
        selection = self.lang_combo.get()
        self.current_lang = "tr" if selection == "Türkçe" else "en"
        self.update_ui_text()

    def update_ui_text(self):
        self.root.title(self.t("title"))
        self.title_label.config(text=self.t("title"))
        self.cred_frame.config(text=self.t("settings"))
        self.email_label.config(text=self.t("email"))
        self.pass_label.config(text=self.t("password"))
        self.server_label.config(text=self.t("server"))
        self.opt_frame.config(text=self.t("options"))
        self.delete_check.config(text=self.t("delete"))
        self.organize_check.config(text=self.t("organize"))
        self.start_btn.config(text=self.t("start"))
        self.open_btn.config(text=self.t("open"))

    def check_license(self):
        # In a real app, you might store this in a file or registry
        # For this demo, we ask every time if not in config
        email = config.EMAIL_USER
        key = config.LICENSE_KEY
        
        valid = False
        if config.LICENSE_SERVER_URL:
             # Online Check
             if email and key:
                 valid = license_manager.validate_license_online(email, key, config.LICENSE_SERVER_URL)
        else:
            # Offline Check
            if email and key:
                valid = license_manager.validate_license(email, key)
        
        if not valid:
            self.prompt_license()

    def prompt_license(self):
        while True:
            email = simpledialog.askstring(self.t("license_check"), self.t("enter_email"))
            if not email:
                messagebox.showerror(self.t("error"), self.t("email_required"))
                self.root.destroy()
                exit()
                
            key = simpledialog.askstring(self.t("license_check"), self.t("enter_key"))
            if not key:
                messagebox.showerror(self.t("error"), self.t("key_required"))
                self.root.destroy()
                exit()

            # Validate
            if config.LICENSE_SERVER_URL:
                if license_manager.validate_license_online(email, key, config.LICENSE_SERVER_URL):
                    messagebox.showinfo(self.t("success"), self.t("online_valid"))
                    config.EMAIL_USER = email
                    config.LICENSE_KEY = key
                    break
                else:
                    messagebox.showerror(self.t("error"), self.t("online_invalid"))
            else:
                if license_manager.validate_license(email, key):
                    messagebox.showinfo(self.t("success"), self.t("license_valid"))
                    config.EMAIL_USER = email
                    config.LICENSE_KEY = key
                    break
                else:
                    messagebox.showerror(self.t("error"), self.t("license_invalid"))

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def update_progress(self, current, total):
        percent = (current / total) * 100
        self.progress_var.set(percent)
        self.root.update_idletasks()

    def open_folder(self):
        if not os.path.exists(config.BACKUP_DIR):
            os.makedirs(config.BACKUP_DIR)
        os.system(f"open {config.BACKUP_DIR}")

    def start_backup_thread(self):
        # Update config with UI values
        config.EMAIL_USER = self.email_entry.get().strip()
        config.EMAIL_PASS = self.pass_entry.get().strip()
        config.IMAP_SERVER = self.server_entry.get().strip()
        config.DELETE_AFTER_BACKUP = self.delete_var.get()
        config.ORGANIZE_BY_DATE = self.organize_var.get()

        self.start_btn.config(state='disabled')
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')
        self.progress_var.set(0)

        thread = threading.Thread(target=self.run_backup)
        thread.start()

    def run_backup(self):
        try:
            backup_manager.backup_emails(
                progress_callback=self.update_progress,
                log_callback=self.log
            )
        except Exception as e:
            self.log(f"Critical Error: {e}")
        finally:
            self.start_btn.config(state='normal')
            messagebox.showinfo(self.t("success"), self.t("success"))

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
