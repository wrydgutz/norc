# norc/main.py
# MIT License © 2025 Wrydrick Gutierrez

from norc.email import gmail_watcher

def main():
    gmail_watcher.start_gmail_watcher()

if __name__ == "__main__":
    main()