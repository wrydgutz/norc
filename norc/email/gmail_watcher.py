# norc/email/gmail_watcher.py
# MIT License © 2025 Wrydrick Gutierrez

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
]

TOKEN_PATH = "secrets/token.pickle"
CREDENTIALS_PATH = "secrets/gmail_client_secret.json"

def authenticate_gmail():
    creds = None

    # Load access token if it exists.
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or login if necessary.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run.
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'wb') as token_file:
            pickle.dump(creds, token_file)

    # Return the authenticated service to be able to use Gmail API going forward.
    service = build("gmail", "v1", credentials=creds)
    return service

def start_gmail_watcher():
    print("Starting Gmail watcher...")

    service = authenticate_gmail()

    # Simple test: list labels
    result = service.users().labels().list(userId="me").execute()
    labels = result.get("labels", [])

    print("Labels:")
    for label in labels:
        print(f" - {label['name']}")

    print("Gmail watcher started successfully.")