# coding: utf-8

import os
import hashlib

from .model import Model


class User(Model):
    _table = 'users'

    def _create_columns(self):
        return super()._create_columns() + [
            {'login': 'TEXT NOT NULL UNIQUE'},
            {'salt': 'BYTEA NOT NULL'},
            {'key': 'BYTEA NOT NULL'},
        ]

    def _create_account(self, login, password):
        salt = os.urandom(64)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return self.insert({
            'login': login,
            'salt': salt,
            'key': key,
        })

    def check_password(self, login, password):
        user = self.select("WHERE login = '%s'" % login)
        if user:
            user = user[0]
            salt = user['salt']
            new_key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            if new_key == user['key'].tobytes():
                return True
        return False


u = User()
u.create_table()

# try:
#     u._create_account('admin', 'password')
# except:
#     pass
