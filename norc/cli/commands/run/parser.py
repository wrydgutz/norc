# norc/cli/commands/run/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import argparse
import sys

import norc.service.run_service as run_service

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
    
    run_service.run()
    sys.exit(0)
