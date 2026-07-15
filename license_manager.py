import hashlib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

SECRET_SALT = "AntArge_Secure_Salt_2024"

def generate_license_key(email):
    """Generates a license key for the given email."""
    raw_string = f"{email.strip().lower()}:{SECRET_SALT}"
    return hashlib.sha256(raw_string.encode()).hexdigest()[:16].upper()

def validate_license(email, key):
    """Checks if the key is valid for the email (Offline Math Check)."""
    expected_key = generate_license_key(email)
    return key.strip().upper() == expected_key

def validate_license_online(email, key, server_url):
    """
    Checks if the key is valid by querying a remote server/file.
    The server should return a JSON or Text list of valid 'email:key' pairs
    OR simply return 'VALID' if the query param matches.
    
    For simplicity, we assume the server returns a list of valid keys/emails.
    """
    if not HAS_REQUESTS:
        return False

    try:
        response = requests.get(server_url, timeout=5)
        if response.status_code == 200:
            # Simple check: Is "email|key" present in the response text?
            # Format in server file: example@mail.com|KEY123
            check_string = f"{email.strip().lower()}|{key.strip().upper()}"
            return check_string in response.text
        return False
    except:
        return False  # Fail safe: Block if server unreachable (or True to allow offline)

if __name__ == "__main__":
    # Test / Admin Utility
    print("--- License Key Generator ---")
    email = input("Enter Email: ")
    print(f"License Key: {generate_license_key(email)}")
    print(f"\n[INFO] For Online Check: Add '{email}|{generate_license_key(email)}' to your server file.")
