# norc/email/watcher.py
# MIT License © 2025 Wrydrick Gutierrez

import os.path

import norc.email.gmail as gmail

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
]

TOKEN_PATH = "secrets/token.pickle"
CREDENTIALS_PATH = "secrets/gmail_client_secret.json"

HISTORY_ID_FILENAME = "history_id.txt"

POLL_INTERVAL_SEC_DEFAULT = 10

class Watcher:
    def __init__(self, email_address, poll_interval_sec=POLL_INTERVAL_SEC_DEFAULT):
        self.email_address = email_address
        self.poll_interval_sec = poll_interval_sec

    def run(self, shutdown_event):
        service = self.authenticate()

        while not shutdown_event.is_set():
            print(f"Watcher ({self.email_address}): Checking new emails...")
            
            history_id = self.load_history_id(service)

            message_ids, new_history_id = self.check_for_new_emails(service, history_id)
            if message_ids:
                print(f"Watcher ({self.email_address}): Found new message IDs: {message_ids}")
            if new_history_id:
                self.save_history_id(new_history_id)
                history_id = new_history_id

            shutdown_event.wait(timeout=self.poll_interval_sec)

        print(f"Watcher ({self.email_address}): stopped.", flush=True)
            
    def authenticate(self):
        creds = gmail.load_token(self.email_address)
        if not gmail.refreshIfNeeded(self.email_address):
            return None
        return gmail.build_service(creds)
    
    def load_history_id(self, service):
        history_id_path = self.get_history_id_path()
        if os.path.exists(history_id_path):
            with open(history_id_path, "r") as file:
                history_id = file.read().strip()
            
            if history_id.isdigit():
                history_id = int(history_id)
            else: # Fallback if history_id isn't valid or readable.
                history_id = gmail.fetch_profile(service).get("historyId")
            return history_id
        
        history_id = gmail.fetch_profile(service).get("historyId")
        return history_id

    def save_history_id(self, history_id):
        with open(self.get_history_id_path(), "w") as file:
            file.write(str(history_id))

    def get_history_id_path(self):
        user_dir = gmail.get_user_directory(self.email_address)
        return os.path.join(user_dir, HISTORY_ID_FILENAME)
    
    def check_for_new_emails(self, service, last_history_id):
        response = gmail.fetch_new_emails(service, last_history_id)

        history = response.get("history", [])
        message_ids = []
        for record in history:
            for msg in record.get("messages", []):
                message_ids.append(msg["id"])

        return message_ids, response.get("historyId")