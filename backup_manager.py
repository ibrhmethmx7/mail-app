import imaplib
import email
from email.header import decode_header
import os
import datetime
import config

def connect_to_mail():
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(config.IMAP_SERVER, config.IMAP_PORT)
        mail.login(config.EMAIL_USER, config.EMAIL_PASS)
        return mail, None
    except Exception as e:
        return None, str(e)

def clean_filename(subject):
    return "".join(c for c in subject if c.isalnum() or c in (' ', '_', '-')).rstrip()

def backup_emails(progress_callback=None, log_callback=None):
    """
    progress_callback: function(current, total)
    log_callback: function(message)
    """
    def log(msg):
        print(msg)
        if log_callback:
            log_callback(msg)

    mail, error = connect_to_mail()
    if not mail:
        log(f"Sunucuya bağlanılamadı: {error}")
        return

    log("Sunucuya bağlanıldı. Gelen kutusu taranıyor...")
    mail.select("inbox")

    # Search for all emails
    status, messages = mail.search(None, "ALL")
    if status != "OK":
        log("E-postalar alınamadı.")
        return

    email_ids = messages[0].split()
    total_emails = len(email_ids)
    log(f"Toplam {total_emails} e-posta bulundu.")

    if not os.path.exists(config.BACKUP_DIR):
        os.makedirs(config.BACKUP_DIR)

    for index, mail_id in enumerate(email_ids):
        try:
            # Update progress
            if progress_callback:
                progress_callback(index + 1, total_emails)

            # Fetch the email
            res, msg = mail.fetch(mail_id, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    # Decode subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    # Get date for folder structure
                    date_tuple = email.utils.parsedate_tz(msg["Date"])
                    if date_tuple:
                        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                        year = str(local_date.year)
                        month = str(local_date.month).zfill(2)
                    else:
                        year = "unknown"
                        month = "unknown"

                    # Create folder path
                    if config.ORGANIZE_BY_DATE:
                        folder_path = os.path.join(config.BACKUP_DIR, year, month)
                    else:
                        folder_path = config.BACKUP_DIR
                        
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    # Save file
                    safe_subject = clean_filename(subject)
                    filename = f"{safe_subject}_{mail_id.decode()}.eml"
                    filepath = os.path.join(folder_path, filename)

                    with open(filepath, "wb") as f:
                        f.write(response[1])
                    
                    log(f"Yedeklendi: {filename}")

                    # Delete from server if configured
                    if config.DELETE_AFTER_BACKUP:
                        mail.store(mail_id, "+FLAGS", "\\Deleted")
                        log(f"Silinmek üzere işaretlendi: {subject}")

        except Exception as e:
            log(f"Hata (ID: {mail_id}): {e}")

    if config.DELETE_AFTER_BACKUP:
        mail.expunge() # Permanently remove deleted emails
        log("İşaretlenen e-postalar sunucudan kalıcı olarak silindi.")
    
    mail.close()
    mail.logout()
    log("İşlem tamamlandı.")

if __name__ == "__main__":
    # Güvenlik uyarısı
    if config.EMAIL_USER == "your_email@example.com":
        print("Lütfen önce config.py dosyasını düzenleyip mail bilgilerinizi girin.")
    else:
        backup_emails()
