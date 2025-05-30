# norc/cli/commands/config/email/accounts/clear/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

COMMAND_NAME = "clear"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="Removes all accounts.")
    
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    print("This command is not implemented yet. (placeholder)")
        
    sys.exit(0)