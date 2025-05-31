# norc/cli/commands/config/email/accounts/list/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

import norc.email.accounts as accounts

COMMAND_NAME = "list"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="List email addresses.")
    
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    accounts.load()
    keys = accounts.load().keys()
    if len(keys) == 0:
        print("No email accounts found.")
        sys.exit(1)

    for email_address in accounts.load().keys():
        print(email_address)

    sys.exit(0)