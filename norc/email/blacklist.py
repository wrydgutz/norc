# norc/email/blacklist.py
# MIT License © 2025 Wrydrick Gutierrez

import os
import re
import json

BLACKLIST_PATH = "secrets/blacklist.json"
EMAIL_ADDRESS_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def load_blacklist(path=BLACKLIST_PATH):
    if not os.path.exists(path):
        return set()
    try:
        with open(path, "r") as file:
            return set(json.load(file))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from blacklist file: {e}")
        return set()
    
def save_blacklist(blacklist, path=BLACKLIST_PATH):
    with open(path, "w") as file:
        json.dump(list(blacklist), file)

def add_email_to_blacklist(email_address):
    email_address = normalize_email_address(email_address)
    blacklist = load_blacklist()
    
    if not is_valid_email(email_address) or email_address in blacklist:
        return False
    
    blacklist.add(email_address)
    save_blacklist(blacklist)
    return True

def normalize_email_address(email_address):
    return email_address.lower()

def is_valid_email(email_address):
    return EMAIL_ADDRESS_REGEX.match(email_address) is not None

def remove_email_from_blacklist(email_address):
    email_address = normalize_email_address(email_address)
    blacklist = load_blacklist()
    if email_address not in blacklist:
        return False
    blacklist.remove(email_address)
    save_blacklist(blacklist)
    return True

def clear_blacklist():
    save_blacklist(set())

def is_blacklisted(email_address):
    email_address = normalize_email_address(email_address)
    blacklist = load_blacklist()
    return email_address in blacklist
