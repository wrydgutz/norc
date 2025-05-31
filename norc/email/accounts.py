# norc/email/accounts.py
# MIT License © 2025 Wrydrick Gutierrez

import os
import re
import json

ACCOUNTS_PATH = "secrets/accounts.json"
EMAIL_ADDRESS_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def load(path=ACCOUNTS_PATH):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from accounts file: {e}")
        return {}
    
def save(accounts, path=ACCOUNTS_PATH):
    with open(path, "w") as file:
        json.dump(accounts, file)

def add(email_address):
    email_address = normalize_email_address(email_address)
    accounts = load()
    
    if not is_valid_email(email_address) or email_address in accounts:
        return False
    
    accounts[email_address] = {}
    save(accounts)
    return True

def normalize_email_address(email_address):
    return email_address.lower()

def is_valid_email(email_address):
    return EMAIL_ADDRESS_REGEX.match(email_address) is not None

def remove(email_address):
    email_address = normalize_email_address(email_address)
    accounts = load()
    if email_address not in accounts:
        return False
        
    del accounts[email_address]
    save(accounts)
    return True

def clear():
    save({})