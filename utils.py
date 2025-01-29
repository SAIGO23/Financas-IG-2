# utils.py
import hashlib
import os
import json

def hash_password(password):
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed_password

def verify_password(stored_password, provided_password):
    salt = stored_password[:32]
    stored_password = stored_password[32:]
    hashed_password = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return hashed_password == stored_password

def update_passwords(file_path):
    with open(file_path, 'r') as file:
        users = json.load(file)

    for user in users:
        plain_password = users[user]['password']
        users[user]['password'] = hash_password(plain_password).hex()

    with open(file_path, 'w') as file:
        json.dump(users, file, indent=4)

if __name__ == "__main__":
    update_passwords('users_db.json')