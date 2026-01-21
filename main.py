import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

chars_to_remove = ['a','b','c','d','e',
                   'f','g','h','i','j',
                   'k','l','m','n','o',
                   'p','q','r','s','t',
                   'u','v','w','x','y',
                   'z','(',')','*','@',
                   '&','{','}','^']

class MyHandler(FileSystemEventHandler):
    def on_modified(self,event):

        if not event.is_directory and event.src_path.endswith('.txt'):

            time.sleep(0.1)
            with open(event.src_path, 'r', encoding='utf-8') as f:
                text = f.read().lower()




    def on_created(self,event):
        pass

if __name__ == "__main__":

    event_handler = MyHandler()

    home = Path.home()
    test_folder = home / 'Downloads' / 'test'
    observer = Observer()
    observer.schedule(event_handler, path=test_folder, recursive=False)
    observer.start()

    try:
        while observer.is_alive():
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    except Exception as e:
        observer.stop()

    observer.join()





