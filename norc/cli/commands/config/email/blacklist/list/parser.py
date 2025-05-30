# norc/cli/commands/config/email/blacklist/list/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

COMMAND_NAME = "list"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="List all items in the blacklist")
    
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    print("Listing blacklist items (placeholder)")
    sys.exit(0)