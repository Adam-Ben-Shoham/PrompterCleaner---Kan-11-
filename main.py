import sys
import time
from pathlib import Path
import os
import winsound
import ctypes

if getattr(sys, 'frozen', False):
    current_dir = Path(sys.executable).parent.resolve()
else:
    current_dir = Path(__file__).parent.resolve()

chars_to_remove = 'abcdefghijklmnopqrstuvwxyz()*@&{}^+'
niqqud_chars = ''.join(chr(c) for c in range(0x0591, 0x05C8))
complete_removal_list = chars_to_remove + niqqud_chars

table = str.maketrans('', '', complete_removal_list)


def clean_text(file_path):

    try:

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().lower()
            cleaned_text = text.translate(table)

        if text == cleaned_text:
            return
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

        winsound.Beep(500, 200)

        log_action(f'Successfully cleaned {file_path}\n')

    except FileNotFoundError:
        log_action(f'{file_path} not found')
    except PermissionError as e:
        log_action(f'Permission Error for: {file_path} error is {e} \n')
    except Exception as e:
        log_action(f'Unknown Error for: {file_path} error: {e} \n')

def log_action(message):
    log_path = current_dir / 'New folder (4)' / 'log.txt'

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
        f.flush()


if __name__ == "__main__":
    watch_path = current_dir

    ctypes.windll.user32.MessageBoxW(0, f"Watching: {watch_path}", "Prompter Tool", 0x40000)


    while True:
        try:
            for file_path in watch_path.glob('*פרומפטר.txt'):
                if file_path.name == 'cleaning_log.txt':
                    continue

                clean_text(file_path)

            time.sleep(1)

        except KeyboardInterrupt:
            break
        except Exception as e:
            log_action(f'Polling loop error: {str(e)}')
            time.sleep(5)
