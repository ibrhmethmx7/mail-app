import os

# Mail Server Configuration
# Kullanıcıdan bu bilgileri alacağız veya buraya girmesini isteyeceğiz.
EMAIL_USER = "your_email@example.com"
EMAIL_PASS = "your_password"
IMAP_SERVER = "mail.example.com"
IMAP_PORT = 993

# Backup Configuration
BACKUP_DIR = "local_backups"
DELETE_AFTER_BACKUP = False  # Güvenlik için varsayılan olarak kapalı, testten sonra açacağız.
ORGANIZE_BY_DATE = True # True: YYYY/MM/Subject.eml, False: Subject.eml
LICENSE_KEY = ""
LICENSE_SERVER_URL = "" # Boş bırakılırsa Offline çalışır. Örn: "https://mysite.com/licenses.txt"
