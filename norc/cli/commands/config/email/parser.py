# norc/cli/commands/config/email/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

from norc.cli.commands.config.email.blacklist import parser as blacklist_command

COMMAND_NAME = "email"
DEST_COMMAND = "email_command"

parser = None
blacklist_parser = None

def build_parser(subparsers):
    global parser, blacklist_parser

    parser = subparsers.add_parser(COMMAND_NAME, description="Manage email settings")

    email_subparsers = parser.add_subparsers(dest=DEST_COMMAND, help="Email commands")
    
    blacklist_command.build_parser(email_subparsers)
    
    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    subcommand = getattr(args, DEST_COMMAND)
    blacklist_command.dispatch(args, subcommand)
    
    print("No config command specified", file=sys.stderr)
    parser.print_help()
    sys.exit(1)