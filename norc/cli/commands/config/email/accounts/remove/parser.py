# norc/cli/commands/config/email/blacklist/accounts/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

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
    
    print("This command is not implemented yet. (placeholder)")
    sys.exit(0)