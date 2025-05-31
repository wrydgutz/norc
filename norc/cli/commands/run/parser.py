# norc/cli/commands/run/parser.py
# MIT License © 2025 Wrydrick Gutierrez

import argparse
import sys
import threading
import time

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
    
    # Start the run service in a separate thread
    shutdown_event = threading.Event()
    worker_thread = threading.Thread(target=run_service.run, args=(shutdown_event,))
    worker_thread.start()

    # Listen for the KeyboardInterrupt to gracefully shut down
    try:
        while not shutdown_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        shutdown_event.set()

    # Wait for the worker thread to finish and exit.
    worker_thread.join()
    sys.exit(0)
