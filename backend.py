import sys
import time
import json
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROPAGATING = False
CONFIG = None

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_modified(self, event):
        if event.is_directory:
            global PROPAGATING
            global CONFIG

            PROPAGATING = False
            try:
                with open('config.json', 'r') as f:
                    CONFIG = json.load(f)
                    print(CONFIG)
            except json.decoder.JSONDecodeError:
                print('error reading ./config.JSON')

            # reload the propagation with the updated CONFIG

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, './config.json', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
