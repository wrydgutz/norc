# norc/service/run_service.py
# MIT License © 2025 Wrydrick Gutierrez

import json
import os
import threading
import time

import norc.email.accounts as email_accounts
import norc.email.blacklist as email_blacklist
import norc.email.gmail as gmail

from google.cloud import pubsub_v1
from collections import defaultdict
from email.utils import parseaddr

PROJECT_ID = "norc-461313"
SUBSCRIPTION_ID = "gmail-notifications-sub"
TOPIC_ID = "gmail-notifications"
TOPIC_NAME = f"projects/{PROJECT_ID}/topics/{TOPIC_ID}"

SERVICE_ACCOUNT_KEY_FILE = "secrets/norc_gmail-pubsub-consumer_key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_KEY_FILE

DAILY_INTERVAL = 24 * 60 * 60

accounts = None
blacklist = None
locks = defaultdict(threading.Lock)

DUMP_DIR = "secrets/dumps"

def run():
    global accounts, blacklist
    accounts = email_accounts.load()
    blacklist = email_blacklist.load_blacklist()

    for email_address in accounts.keys():
        service = authenticate(email_address)
        register_watch_if_needed(service, email_address)
        refresh_watcher_periodically(email_address, DAILY_INTERVAL)

    # Start listening for Gmail notifications
    listen_for_gmail_notifications()

def authenticate(email_address):
    creds = gmail.load_token(email_address)
    if not gmail.refreshIfNeeded(email_address):
        return None
    return gmail.build_service(creds)

def register_watch_if_needed(service, email_address):
    global accounts
    
    if accounts[email_address].get("lastHistoryId") and accounts[email_address].get("expiration"):
        print(f"Watch already registered for '{email_address}'. Skipping registration.")
        # TODO: Refresh if about to expire.
        return
    
    response = gmail.watch(service, email_address, TOPIC_NAME)
    accounts[email_address]["lastHistoryId"] = response["historyId"]
    accounts[email_address]["expiration"] = response["expiration"]
    email_accounts.save(accounts)
    print(f"Registered watch for '{email_address}' with history ID: {response['historyId']} and expiration: {response['expiration']}")

def refresh_watcher_periodically(email_address, interval = 10):
    thread = threading.Thread(target=do_refresh_watcher_periodically, args=(email_address, interval,), daemon=True)
    thread.start()
    
def do_refresh_watcher_periodically(email_address, interval = 10):
    while True:
        time.sleep(interval)
        gmail.refresh(email_address)
        print(f"{email_address}: Watcher refreshed.")

def listen_for_gmail_notifications():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    print(f"Listening for messages on {subscription_path}...\n")
    
    streaming_pull_future = subscriber.subscribe(
        subscription_path, 
        callback=process_gmail_notification, 
        flow_control=pubsub_v1.types.FlowControl(max_messages=100)
    )

    with subscriber:
        try:
            streaming_pull_future.result()  # Blocks until KeyboardInterrupt or error
        except KeyboardInterrupt:
            streaming_pull_future.cancel()  # Triggers the shutdown of the subscriber
            streaming_pull_future.result()  # Wait for the callback to complete
            print("Shutdown gracefully.")

def process_gmail_notification(message):
    global accounts

    try:
        email_address, notif_history_id = decode_message(message)
    except Exception as e:
        print(f"Error processing Pub/Sub message: {e}")
        print(f"Message data: {message.data.decode('utf-8', errors='ignore')}")
        message.ack() # Acknowledge to prevent reprocessing bad messages endlessly
        return
    
    if not email_address or not notif_history_id:
        print("Invalid notification payload. Missing emailAddress or historyId.")
        message.ack()
        return
    
    print(f"{email_address} ({notif_history_id}): Notified.")
    
    if email_address not in accounts.keys():
        print(f"{email_address} ({notif_history_id}): Email address not found in accounts. Skipping.")
        message.ack()
        return

    with locks[email_address]: # Aquire lock per email address
        last_history_id = accounts[email_address]["lastHistoryId"]
        print(f"{email_address} ({notif_history_id}): Checking for changes since {last_history_id}.")
        
        if int(notif_history_id) <= int(last_history_id):
            print(f"{email_address} ({notif_history_id}): History ID {notif_history_id} already processed. Skipping.")
            message.ack()
            return

        # Get Gmail service for the specific user
        service = authenticate(email_address)
        if not service:
            print(f"{email_address} ({notif_history_id}): Could not get Gmail service. Will retry later.")
            message.nack() # Negative acknowledge, Pub/Sub will re-deliver
            return

        # Fetch history changes
        response = gmail.fetch_new_emails(service, last_history_id, email_address)

        # TODO: Better if this could be specified via CLI arg.
        # Dump response to a file for debugging purposes
        # os.makedirs(DUMP_DIR, exist_ok=True)
        # dump_file = os.path.join(DUMP_DIR, f"{notif_history_id}.json")
        # with open(dump_file, 'w') as f:
        #     json.dump(response, f, indent=2)

        history = response.get("history", [])
        if not history:
            print(f"{email_address} ({notif_history_id}): No new changes found since {last_history_id}.")
        
        # Update the last history ID with the latest one in the response after fetching new emails.
        new_history_id = response.get("historyId", notif_history_id)

        message_ids = get_message_ids(history)
        if message_ids:
            print(f"{email_address} ({notif_history_id}): Found new messages.")

        process_messages(service, email_address, message_ids)

        print(f"{email_address} ({notif_history_id}): Updating last history id with {new_history_id}.")
        accounts[email_address]["lastHistoryId"] = new_history_id
        email_accounts.save(accounts)
        message.ack()
        
def decode_message(message):
    decoded_data = message.data.decode('utf-8')
    notification_payload = json.loads(decoded_data)
    
    email_address = notification_payload.get('emailAddress')
    history_id = notification_payload.get('historyId')
    return email_address, history_id

def get_message_ids(history):
    message_ids = []
    for record in history:
        messagesAdded = record.get("messagesAdded", [])
        for msgAdded in messagesAdded:
            msg = msgAdded.get("message")
            message_ids.append(msg["id"])
    return message_ids

def process_messages(service, email_address, message_ids):
    for msg_id in message_ids:
        try:
            response = gmail.fetch_message(service, email_address, msg_id)
        except Exception as exception:
            print(f"{email_address}: Failed to fetch message {msg_id}: {exception}")
            continue
        
        # TODO: Better if this could be specified via CLI arg.
        # dump(response, "messages", msg_id)

        from_address, subject = extract_info(response)
        if from_address in blacklist:
            gmail.mark_as_read(service, email_address, msg_id)
            print(f"{email_address}: Message blacklisted and marked as read ({from_address}, '{subject}').")
            continue

        print(f"{email_address}: Message ignored ({from_address}, '{subject}')")
        

def extract_info(message):
    headers = message["payload"]["headers"]
    from_address, subject = None, None
    for header in headers:
        if header["name"].lower() == "from":
            name, addr = parseaddr(header["value"])
            from_address = addr
        elif header["name"].lower() == "subject":
            subject = header["value"]
    return from_address, subject

def dump(response, dir, name):
    dump_dir = os.path.join(DUMP_DIR, dir)
    os.makedirs(dump_dir, exist_ok=True)
    dump_file = os.path.join(dump_dir, f"{name}.json")
    with open(dump_file, 'w') as f:
        json.dump(response, f, indent=2)
