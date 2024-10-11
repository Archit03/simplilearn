import hashlib
import os

class User:
    creds_file = 'users.txt'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def hash_password(password):
        username = input("Enter a username:")
        password = input("Enter a password:")
    
    @classmethod
    def register(cls):
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        if os.path.exists(cls.creds_file):
            with open(cls.creds_file, 'r') as f:
                for line in f:
                    stored_username, _ = line.strip().split('')
                    if stored_username == username:
                        print("Username already exists! Please pick another.")
                        return None
        user = cls(username,password)

        with open(cls.creds_file, 'a') as f:
            f.write(f"{user.username}:{user.password}\n")
        print("Registeration successful")
        return user
    
    @classmethod
    def login(cls):
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        if os.path.exists(cls.creds_file):
            with open(cls.creds_file, 'r') as f:
                for line in f:
                    stored_username, stored_password = line.strip().split('')
                    if stored_username == username and stored_password == cls.hash_password(password):
                        print("login successful!")
                        return cls(username, password)
        print("Invalid username or password, please check your creds.")
        return None
     

