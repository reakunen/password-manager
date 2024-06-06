import os
import json
import bcrypt
import base64
from tkinter import simpledialog
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

PASSWORD_FILE = './passwords/password.json'


class PasswordMethods:
    def __init__(self, master_password):
        self.vault_data = self.load_vault()
        if 'salt' not in self.vault_data:
            self.vault_data['salt'] = base64.urlsafe_b64encode(os.urandom(16)).decode()
            self.save_vault()
        self.key = self.derive_key(master_password, self.vault_data['salt'])
        self.fernet = Fernet(self.key)

    def derive_key(self, master_password, salt):
        salt = base64.urlsafe_b64decode(salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(master_password.encode())
        return base64.urlsafe_b64encode(key)

    def load_vault(self):
        if not os.path.exists(PASSWORD_FILE):
            with open(PASSWORD_FILE, 'w') as file:
                json.dump({'vault': [], 'salt': ''}, file)
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)

    def save_vault(self):
        with open(PASSWORD_FILE, 'w') as file:
            json.dump(self.vault_data, file, indent=4)

    def popup_entry(self, heading):
        answer = simpledialog.askstring("Enter details", heading)
        return answer

    def add_password(self, vault_screen):
        platform = self.popup_entry("Platform")
        userid = self.popup_entry("Username")
        password = self.popup_entry("Password")

        encrypted_password = self.encrypt_password(password)

        new_entry = {"id": len(self.vault_data['vault']) + 1, "platform": platform, "userid": userid, "password": encrypted_password}
        self.vault_data['vault'].append(new_entry)
        self.save_vault()
        vault_screen()

    def update_password(self, id, vault_screen):
        password = self.popup_entry("Enter New Password")
        encrypted_password = self.encrypt_password(password)
        for entry in self.vault_data['vault']:
            if entry['id'] == id:
                entry['password'] = encrypted_password
                break
        self.save_vault()
        vault_screen()

    def remove_password(self, id, vault_screen):
        self.vault_data['vault'] = [entry for entry in self.vault_data['vault'] if entry['id'] != id]
        self.save_vault()
        vault_screen()

    def encrypt_password(self, password):
        return self.fernet.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        return self.fernet.decrypt(encrypted_password.encode()).decode()
