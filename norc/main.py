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
    
    run_parser = subparsers.add_parser(
        "run",
        description=(
            "Starts the entire program:\n"
            "  - Starts the Gmail watcher(s)\n"
            "  - Processes new emails\n"
            "  - Marks promotional emails as read (if configured)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    config_parser = subparsers.add_parser(
        "config",
        description=(
            "Configures the program:\n"
            "  - Sets up the Gmail watcher(s)\n"
            "  - Configures email processing rules\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    config_subparsers = config_parser.add_subparsers(dest="config_command",
                                                     help="Config commands")
    
    email_parser = config_subparsers.add_parser(
        "email",
        description="Manage email settings"
    )

    email_subparsers = email_parser.add_subparsers(dest="email_command",
                                                   help="Email commands")
    
    blacklist_parser = email_subparsers.add_parser(
        "blacklist",
        help="Manage the blacklist"
    )
    blacklist_subparsers = blacklist_parser.add_subparsers(dest="blacklist_command",
                                                           help="Blacklist commands")

    blacklist_add = blacklist_subparsers.add_parser("add", help="Add an item to the blacklist")
    blacklist_add.add_argument("email", type=str, help="Email address to add to the blacklist")

    blacklist_remove= blacklist_subparsers.add_parser("remove", help="Remove an item from the blacklist")
    blacklist_remove.add_argument("email", type=str, help="Email address to add to the blacklist")

    blacklist_subparsers.add_parser("list", help="List all items in the blacklist")
    
    args = parser.parse_args()

    if args.command == "run":
        gmail_watcher.start_gmail_watcher()
        sys.exit(0)
    elif args.command == "config":
        if args.config_command == "email":
            if args.email_command == "blacklist":
                if args.blacklist_command == "add":
                    print(f"Added to blacklist: {args.email}")
                    sys.exit(0)
                elif args.blacklist_command == "remove":
                    print(f"Removed from blacklist: {args.email}")
                    sys.exit(0)
                elif args.blacklist_command == "list":
                    print("Listing blacklist items (placeholder)")
                    sys.exit(0)
                else:
                    print("No blacklist command specified", file=sys.stderr)
                    blacklist_parser.print_help()
                    sys.exit(1)
            else:
                print("No config command specified", file=sys.stderr)
                email_parser.print_help()
                sys.exit(1)
        else:
            print("No config command specified", file=sys.stderr)
            config_parser.print_help()
            sys.exit(1)
    elif args.command is None:
        parser.print_help()
        sys.exit(1)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
        
if __name__ == "__main__":
    main()