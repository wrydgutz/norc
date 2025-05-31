# norc/cli/commands/config/email/blacklist/accounts/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys
import os

import norc.email.gmail as gmail
import norc.email.accounts as accounts

COMMAND_NAME = "remove"
ARG_EMAIL_ADDRESS = "email_address"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="Remove an email account.")
    parser.add_argument(ARG_EMAIL_ADDRESS, type=str, help="Email address of the account to be removed.")

    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    arg_email_address = getattr(args, ARG_EMAIL_ADDRESS)
    token_path = gmail.get_token_path(arg_email_address)
    os.remove(token_path)
    accounts.remove(arg_email_address)
    print(f"'{arg_email_address}' removed.")
    sys.exit(0)