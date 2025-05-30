# norc/cli/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import argparse
import sys

from norc.cli.commands.run import parser as run_command
from norc.cli.commands.config import parser as config_command

parser = None

def build_parser():
    global parser

    parser = argparse.ArgumentParser(
        description="Norc - Silent Automation Assistant"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    run_command.build_parser(subparsers)
    config_command.build_parser(subparsers)
    
    return parser

def dispatch(args):
    run_command.dispatch(args, args.command)
    config_command.dispatch(args, args.command)

    parser.print_help()
    sys.exit(1)
