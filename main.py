import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

chars_to_remove = 'abcdefghijklmnopqrstuvwxyz()*@&{}^'
niqqud_chars = ''.join(chr(c) for c in range(0x05B0, 0x05C8))
complete_removal_list = chars_to_remove + niqqud_chars

table = str.maketrans('', '', complete_removal_list)

class MyHandler(FileSystemEventHandler):

    def clean_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().lower()
            cleaned_text = text.translate(table)

        if text == cleaned_text:
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

    def on_modified(self,event):

        if 'cleaning_log.txt' in event.src_path:
            return


        if not event.is_directory and event.src_path.endswith('ר.txt'):
            log_action(f'Cleaning {event.src_path} \n')
            time.sleep(0.5)
            self.clean_text(event.src_path)



    def on_created(self,event):
        pass

def log_action(message):
    log_path = home / 'Downloads' / 'test' / 'cleaning_log.txt'
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a",encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
        f.flush()

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





