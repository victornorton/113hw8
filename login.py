import os
import pickle
import hashlib
import secrets
import base64

class LoginManager:
    def __init__(self, path='login'):
        self.path = path
        self.data = {'users': {}, 'deleted': []}
        self._load()

    def _load(self):
        if not os.path.exists(self.path):
            self._save()
            return
        try:
            with open(self.path, 'rb') as f:
                self.data = pickle.load(f)
        except Exception:
            self.data = {'users': {}, 'deleted': []}

    def _save(self):
        dirpath = os.path.dirname(os.path.abspath(self.path))
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        with open(self.path, 'wb') as f:
            pickle.dump(self.data, f)

    def _hash_password(self, password, salt=None):
        if salt is None:
            salt = secrets.token_bytes(16)
        else:
            salt = base64.b64decode(salt)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 200000)
        return base64.b64encode(salt).decode('utf-8'), base64.b64encode(key).decode('utf-8')

    def create_user(self, username, password):
        username = username.strip()
        if not username:
            return False, 'Username cannot be blank.'
        if username in self.data['users']:
            return False, 'That name is already taken. Please try again.'
        deleted_before = username in self.data['deleted']
        salt, hashed = self._hash_password(password)
        self.data['users'][username] = {'salt': salt, 'hash': hashed}
        if deleted_before:
            message = 'You cannot recover what has been lost.'
        else:
            message = 'Account created successfully.'
        self._save()
        return True, message

    def verify(self, username, password):
        if username not in self.data['users']:
            return False
        entry = self.data['users'][username]
        salt = entry['salt']
        _, hashed = self._hash_password(password, salt)
        return hashed == entry['hash']

    def delete_user(self, username):
        if username in self.data['users']:
            del self.data['users'][username]
            if username not in self.data['deleted']:
                self.data['deleted'].append(username)
            self._save()
            return True
        return False
