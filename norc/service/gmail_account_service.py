# norc/service/gmail_account_service.py
# MIT License © 2025 Wrydrick Gutierrez

import norc.email.gmail as gmail
import norc.email.accounts as accounts

def authenticate_and_add_account():

    service, creds = gmail.authenticate()
    profile = gmail.fetch_profile(service)
    email_address = profile["emailAddress"]
    gmail.save_token(email_address, creds)
    accounts.add(email_address)
    return email_address