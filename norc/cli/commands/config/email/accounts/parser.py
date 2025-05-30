# norc/cli/commands/config/email/accounts/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import sys

from norc.cli.commands.config.email.accounts.add import parser as add_command
from norc.cli.commands.config.email.accounts.remove import parser as remove_command
from norc.cli.commands.config.email.accounts.list import parser as list_command
from norc.cli.commands.config.email.accounts.clear import parser as clear_command

COMMAND_NAME = "accounts"
DEST_COMMAND = "accounts_command"

parser = None

def build_parser(subparsers):
    global parser

    parser = subparsers.add_parser(
        COMMAND_NAME,
        help="Manage Email accounts"
    )
    accounts_subparsers = parser.add_subparsers(dest=DEST_COMMAND, help="Available commands")

    add_command.build_parser(accounts_subparsers)
    remove_command.build_parser(accounts_subparsers)
    list_command.build_parser(accounts_subparsers)
    clear_command.build_parser(accounts_subparsers)

    return parser

def dispatch(args, command):
    if command != COMMAND_NAME:
        return
    
    subcommand = getattr(args, DEST_COMMAND)
    add_command.dispatch(args, subcommand)
    remove_command.dispatch(args, subcommand)
    list_command.dispatch(args, subcommand)
    clear_command.dispatch(args, subcommand)
    
    print("No command specified", file=sys.stderr)
    parser.print_help()
    sys.exit(1)