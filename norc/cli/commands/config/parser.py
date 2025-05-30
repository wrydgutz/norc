# norc/cli/commands/config/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import argparse
import sys

from norc.cli.commands.config.email import parser as email_command

COMMAND_NAME = "config"
DEST_COMMAND = "config_command"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(
        COMMAND_NAME,
        description=(
            "Configures the program:\n"
            "  - Sets up the Gmail watcher(s)\n"
            "  - Configures email processing rules\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    config_subparsers = parser.add_subparsers(dest=DEST_COMMAND, help="Available commands")

    email_command.build_parser(config_subparsers)
    
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    subcommmand = getattr(args, DEST_COMMAND)
    email_command.dispatch(args, subcommmand)

    print("No config command specified", file=sys.stderr)
    parser.print_help()
    sys.exit(1)