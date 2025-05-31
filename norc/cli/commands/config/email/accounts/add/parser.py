# norc/cli/commands/config/email/accounts/add/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

import norc.service.gmail_account_service as gmail

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
    
    email_address = gmail.authenticate_and_add_account()
    print(f"'{email_address}' authenticated and added.")

    sys.exit(0)
