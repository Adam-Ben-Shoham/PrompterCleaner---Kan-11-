import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import winsound
import ctypes

if getattr(sys, 'frozen', False):
    current_dir = Path(sys.executable).parent.resolve()
else:
    current_dir = Path(__file__).parent.resolve()

chars_to_remove = 'abcdefghijklmnopqrstuvwxyz()*@&{}^'
niqqud_chars = ''.join(chr(c) for c in range(0x05B0, 0x05C8))
complete_removal_list = chars_to_remove + niqqud_chars

table = str.maketrans('', '', complete_removal_list)


class MyHandler(FileSystemEventHandler):

    def clean_text(self, file_path):

        try:

            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read().lower()
                cleaned_text = text.translate(table)

            if text == cleaned_text:
                return

            temp_file = str(file_path) + '.tmp'

            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)

            os.replace(temp_file, file_path)
            winsound.Beep(500, 200)

            log_action(f'Successfully cleaned {file_path}\n')

        except FileNotFoundError:
            log_action(f'{file_path} not found')
        except PermissionError:
            log_action(f'Permission Error for: {file_path} \n')
        except Exception as e:
            log_action(f'Unknown Error for: {file_path} \n')

    def on_modified(self, event):

        if 'cleaning_log.txt' in event.src_path or event.src_path.endswith('.tmp'):
            return

        if not event.is_directory and event.src_path.lower().endswith('פרומפטר.txt'):
            time.sleep(0.7)
            self.clean_text(event.src_path)

    def on_created(self, event):
        self.on_modified(event)


def log_action(message):
    log_path = current_dir / 'cleaning_log.txt'

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
        f.flush()


if __name__ == "__main__":
    watch_path = str(current_dir)
    event_handler = MyHandler()

    ctypes.windll.user32.MessageBoxW(0, f"Watching: {watch_path}", "Prompter Tool", 0x40000)

    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=False)
    observer.start()

    try:
        while observer.is_alive():
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    except Exception as e:
        observer.stop()

    observer.join()
