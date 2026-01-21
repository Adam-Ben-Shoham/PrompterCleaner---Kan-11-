import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self,event):
        if not event.is_directory and event.src_path.endswith('.txt'):
            self.read_file_content(event.src_path)

    def read_file_content(self,file_path):
        with open(file_path,'w',encoding='utf-8') as f:
            content = f.read()
            print(content)

    def on_created(self,event):
        pass


