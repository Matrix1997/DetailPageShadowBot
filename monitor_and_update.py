import time
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, filename, callback):
        self.filename = filename
        self.callback = callback

    def on_modified(self, event):
        if event.src_path == self.filename:
            self.callback()

def transform_code(main_py_content):
    # 提取和转换代码的逻辑
    def extract_try_block(content):
        try_start = content.find('try:')
        try_end = content.find('finally:', try_start)
        if try_start != -1 and try_end != -1:
            return content[try_start + len('try:'):try_end].strip()
        return ""
    
    try_block = extract_try_block(main_py_content)

    # Splitting the try block into lines and removing two levels of indentation
    lines = try_block.split('\n')
    adjusted_lines = [line[8:] if line.startswith("        ") else line for line in lines]  # Removing two levels of indentation

    # Reassembling the code block with adjusted indentation
    adjusted_try_block = '\n'.join(adjusted_lines)

    # Normalizing the try block (replacing \n with \r\n and adding '10:' at the beginning)
    transformed_code = "10:" + adjusted_try_block.replace("\n", "\r\n")

    return transformed_code

def update_json_file():
    with open('main.py', 'r', encoding='utf-8') as file:
        main_py_content = file.read()
    
    transformed_code = transform_code(main_py_content)

    with open('.dev/main.flow.json', 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data['blocks'][0]['inputs']['snippet']['value'] = transformed_code
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def monitor_file_changes():
    path = '.'  # 当前目录
    filename = os.path.join(path, 'main.py')
    event_handler = FileMonitorHandler(filename, update_json_file)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    monitor_file_changes()
