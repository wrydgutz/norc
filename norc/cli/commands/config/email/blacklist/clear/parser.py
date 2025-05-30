# norc/cli/commands/config/email/blacklist/clear/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

from norc.email.blacklist import clear_blacklist

COMMAND_NAME = "clear"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="Removes all items from the blacklist")
    
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    clear_blacklist()
    print("Blacklist cleared successfully.")
        
    sys.exit(0)