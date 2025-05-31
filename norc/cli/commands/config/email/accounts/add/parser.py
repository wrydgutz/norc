# norc/cli/commands/config/email/accounts/add/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

import norc.email.gmail as gmail
import norc.email.accounts as accounts

COMMAND_NAME = "add"
ARG_EMAIL_ADDRESS = "email_address"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="Authenticates an account and adds it to the list.")
    
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    service, creds = gmail.authenticate()
    profile = gmail.fetch_profile(service)
    email_address = profile["emailAddress"]
    gmail.save_token(email_address, creds)

    print(f"Authenticated as {email_address}")

    accounts.add(email_address)
    print(f"'{email_address}' authenticated and added.")
    sys.exit(0)
