# norc/cli/commands/run/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import argparse
import sys

from norc.email import gmail_watcher

COMMAND_NAME = "run"

def build_parser(subparsers):
    parser = subparsers.add_parser(
        COMMAND_NAME,
        description=(
            "Starts the entire program:\n"
            "  - Starts the Gmail watcher(s)\n"
            "  - Processes new emails\n"
            "  - Marks promotional emails as read (if configured)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    gmail_watcher.start_gmail_watcher()
    sys.exit(0)