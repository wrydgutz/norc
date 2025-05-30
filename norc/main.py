# norc/main.py
# MIT License © 2025 Wrydrick Gutierrez

import argparse
import sys

from norc.email import gmail_watcher

def main():
    parser = argparse.ArgumentParser(
        description="Norc - Silent Automation Assistant"
    )
    subparsers = parser.add_subparsers(dest="command",
                                       help="Available commands")
    
    watch_parser = subparsers.add_parser(
        "run",
        description=(
            "Starts the entire program:\n"
            "  - Starts the Gmail watcher(s)\n"
            "  - Processes new emails\n"
            "  - Marks promotional emails as read (if configured)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    args = parser.parse_args()

    if args.command == "run":
        gmail_watcher.start_gmail_watcher()
        sys.exit(0)
    elif args.command is None:
        parser.print_help()
        sys.exit(1)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
        
if __name__ == "__main__":
    main()