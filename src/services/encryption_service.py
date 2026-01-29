import os
from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY")
        if not self.key:
            # Fallback or raise error in production
            self.cipher = None
        else:
            self.cipher = Fernet(self.key.encode())

    def encrypt(self, text):
        if not self.cipher or not text:
            return text
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, encrypted_text):
        if not self.cipher or not encrypted_text:
            return encrypted_text
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except:
            return None
