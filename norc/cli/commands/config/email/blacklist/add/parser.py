# norc/cli/commands/config/email/blacklist/add/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

COMMAND_NAME = "add"
ARG_EMAIL_ADDRESS = "email_address"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="Add an item to the blacklist")
    parser.add_argument(ARG_EMAIL_ADDRESS, type=str, help="Email address to add to the blacklist")

    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    arg_email_address = getattr(args, ARG_EMAIL_ADDRESS)
    print(f"Added to blacklist: {arg_email_address}")
    sys.exit(0)