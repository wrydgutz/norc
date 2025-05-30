# norc/cli/commands/config/email/blacklist/list/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

from norc.email.blacklist import load_blacklist

COMMAND_NAME = "list"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="List all items in the blacklist")
    
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    blacklist = load_blacklist()
    if len(blacklist) == 0:
        print("Blacklist is empty.")
        sys.exit(0)
    
    for email_address in blacklist:
        print(email_address)
        
    sys.exit(0)