from cryptography.fernet import Fernet

def generate_key():
    """Generate a random key."""
    return Fernet.generate_key()

def encrypt_message(message, key):
    """Encrypt a message using the provided key."""
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    """Decrypt a message using the provided key."""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()