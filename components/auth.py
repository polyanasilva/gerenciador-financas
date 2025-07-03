import pandas as pd
import hashlib

USERS_FILE = "users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    try:
        users = pd.read_csv(USERS_FILE)
        hashed = hash_password(password)
        user_row = users[(users['username'] == username) & (users['password'] == hashed)]
        return not user_row.empty
    except FileNotFoundError:
        return False

def create_user(username, password):
    hashed = hash_password(password)
    new_user = pd.DataFrame([[username, hashed]], columns=["username", "password"])
    try:
        users = pd.read_csv(USERS_FILE)
        if username in users["username"].values:
            return False
        users = pd.concat([users, new_user], ignore_index=True)
    except FileNotFoundError:
        users = new_user
    users.to_csv(USERS_FILE, index=False)
    return True
