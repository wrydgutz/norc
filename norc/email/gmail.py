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

ACCOUNTS_DIR = "secrets/accounts"
TOKEN_FILENAME = "token.pickle"

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

    # If already valid, or can't be refreshed, no need to refresh
    if creds.valid or not creds.refresh_token:
        return True
    
    # Refresh if possible
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        return True
    
    return False

def refresh(email_address):
    creds = load_token(email_address)
    creds.refresh(Request())
    save_token(email_address, creds)

def get_token_path(email_address):
    token_path = os.path.join(get_user_directory(email_address), TOKEN_FILENAME)
    os.makedirs(os.path.dirname(token_path), exist_ok=True)
    return token_path

def get_user_directory(email_address):
    return os.path.join(ACCOUNTS_DIR, sanitize_email(email_address))

def sanitize_email(email_address):
    return email_address.replace("@", "_").replace(".", "_")

def watch(gmail_service, user_id, topic_name):    
    try:
        response = gmail_service.users().watch(
            userId=user_id,
            body={
                'topicName': topic_name
            }
        ).execute()
        
        return response
        
    except Exception as e:
        print(f"Error registering watch for {user_id}: {e}")
        return None

def fetch_profile(service, userId="me"):
    return service.users().getProfile(userId=userId).execute()

def fetch_new_emails(service, startHistoryId, userId="me", historyTypes=["messageAdded"]):
    return service.users().history().list(
        userId=userId,
        startHistoryId=startHistoryId,
        historyTypes=historyTypes
    ).execute()

def fetch_message(service, userId, message_id, format="full"):
    return service.users().messages().get(
        userId=userId,
        id=message_id,
        format=format
    ).execute()

def mark_as_read(service, userId, message_id):
    return service.users().messages().modify(
        userId=userId,
        id=message_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()