# norc/email/gmail.py
# MIT License © 2025 Wrydrick Gutierrez

import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
]

TOKEN_DIR = "secrets/tokens"
CLIENT_SECRET_PATH = "secrets/gmail_client_secret.json"

ACCOUNTS_PATH = "secrets/accounts.json"

def build_service(credentials):
    return build("gmail", "v1", credentials=credentials)

def authenticate():
    # Login to Gmail
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    creds = flow.run_local_server(port=0)
    service = build_service(creds)
    return service, creds

def save_token(email_address, creds):
    token_path = get_token_path(email_address)
    os.makedirs(os.path.dirname(token_path), exist_ok=True)
    with open(token_path, "wb") as token_file:
        pickle.dump(creds, token_file)

def load_token(email_address):
    token_path = get_token_path(email_address)
    if not os.path.exists(token_path):
        return None
    
    with open(token_path, "rb") as token:
        creds = pickle.load(token)
        return creds

def refreshIfNeeded(email_address):
    creds = load_token(email_address)
    if not creds:
        print(f"No credentials found for {email_address}. Please authenticate first.")
        return False

    if creds.valid or not creds.expired or not creds.refresh_token:
        return True
    
    creds.refresh(Request())
    return True

def get_token_path(email_address):
    token_path = os.path.join(TOKEN_DIR, get_token_filename(email_address))
    return token_path

def get_token_filename(email_address):
    return email_address.replace("@", "_").replace(".", "_") + ".pickle"

def fetch_profile(service, userId="me"):
    return service.users().getProfile(userId=userId).execute()

def fetch_new_emails(service, startHistoryId, userId="me", historyTypes=["messageAdded"]):
    return service.users().history().list(
        userId=userId,
        startHistoryId=startHistoryId,
        historyTypes=historyTypes
    ).execute()