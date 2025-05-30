# norc/cli/commands/config/email/blacklist/remove/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

from norc.email.blacklist import remove_email_from_blacklist

COMMAND_NAME = "remove"
ARG_EMAIL_ADDRESS = "email_address"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="Remove an item from the blacklist")
    parser.add_argument(ARG_EMAIL_ADDRESS, type=str, help="Email address to remove from the blacklist")

    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    arg_email_address = getattr(args, ARG_EMAIL_ADDRESS)
    if remove_email_from_blacklist(arg_email_address):
        print(f"Removed from blacklist: {arg_email_address}")
        sys.exit(0)
    else:
        sys.exit(f"{arg_email_address} not found in blacklist.")