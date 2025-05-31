# norc/cli/commands/config/email/accounts/clear/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys
import os
import shutil

import norc.email.gmail as gmail
import norc.email.accounts as accounts

COMMAND_NAME = "clear"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(COMMAND_NAME, help="Removes all accounts.")
    
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    if os.path.exists(gmail.ACCOUNTS_DIR):
        shutil.rmtree(gmail.ACCOUNTS_DIR)
    accounts.clear()
    print("All email accounts cleared.")
    sys.exit(0)