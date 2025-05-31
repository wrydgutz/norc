# norc/service/run_service.py
# MIT License © 2025 Wrydrick Gutierrez

import threading

import norc.email.watcher as watcher
import norc.email.accounts as email_accounts

def run(shutdown_event):
    threads = []
    accounts = email_accounts.load()

    for email_address in accounts.keys():
        watcher_obj = watcher.Watcher(email_address)
        thread = threading.Thread(target=watcher_obj.run, args=(shutdown_event,))
        thread.start()
        threads.append(thread)

    print("All watchers started in the background.")

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All watchers have finished running. Exiting the run service.")
    
