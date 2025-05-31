# norc/cli/commands/config/email/accounts/add/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

import norc.email.accounts as accounts

COMMAND_NAME = "add"
ARG_EMAIL_ADDRESS = "email_address"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="Authenticates an account and adds it to the list.")
    parser.add_argument(ARG_EMAIL_ADDRESS, type=str, help="Email address to authenticate and add.")

    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    arg_email_address = getattr(args, ARG_EMAIL_ADDRESS)
    accounts.add(arg_email_address)
    
    print(f"'{arg_email_address}' added.")
    sys.exit(0)
