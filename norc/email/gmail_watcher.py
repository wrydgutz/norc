# norc/email/gmail_watcher.py
# MIT License © 2025 Wrydrick Gutierrez

import os.path
import pickle
import time

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
]

TOKEN_PATH = "secrets/token.pickle"
CREDENTIALS_PATH = "secrets/gmail_client_secret.json"

HISTORY_ID_PATH = "secrets/history_id.txt"

def authenticate_gmail():
    creds = None

    # Load access token if it exists.
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
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
        with open(TOKEN_PATH, "wb") as token_file:
            pickle.dump(creds, token_file)

    # Return the authenticated service to be able to use Gmail API going forward.
    service = build("gmail", "v1", credentials=creds)
    return service

def fetch_profile(service, userId="me"):
    return service.users().getProfile(userId=userId).execute()

def fetch_new_emails(service, startHistoryId, userId="me", historyTypes=["messageAdded"]):
    return service.users().history().list(
        userId=userId,
        startHistoryId=startHistoryId,
        historyTypes=historyTypes
    ).execute()

def load_history_id(service):
    if os.path.exists(HISTORY_ID_PATH):
        with open(HISTORY_ID_PATH, "r") as f:
            history_id = f.read().strip()
        if history_id.isdigit():
            history_id = int(history_id)
        else: # Fallback
            history_id = fetch_profile(service).get("historyId")
    else:
        history_id = fetch_profile(service).get("historyId")
        save_history_id(history_id)
    return history_id

def save_history_id(history_id):
    os.makedirs(os.path.dirname(HISTORY_ID_PATH), exist_ok=True)
    with open(HISTORY_ID_PATH, "w") as f:
        f.write(str(history_id))

def check_for_new_emails(service, last_history_id):
    response = fetch_new_emails(service, last_history_id)

    history = response.get("history", [])
    message_ids = []
    for record in history:
        for msg in record.get("messages", []):
            message_ids.append(msg["id"])

    return message_ids, response.get("historyId")

def start_gmail_watcher():
    print("Starting Gmail watcher...")

    print("Authenticating with Gmail...")
    service = authenticate_gmail()
    print("Authenticated successfully.")

    history_id = load_history_id(service)
    print(f"Current history ID: {history_id}")

    print("Gmail watcher started successfully.")

    try:
        while True:
            print("Polling for new emails...")
            message_ids, new_history_id = check_for_new_emails(service, history_id)
            if message_ids:
                print(f"Found new message IDs: {message_ids}")
            # Save the updated history ID for next poll
            if new_history_id:
                save_history_id(new_history_id)
                history_id = new_history_id
            time.sleep(10)
    except KeyboardInterrupt:
        print("Gmail watcher stopped by user.")