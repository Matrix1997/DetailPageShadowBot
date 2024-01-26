import time
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, filename, callback, debounce_interval):
        self.filename = filename
        self.callback = callback
        self.debounce_interval = debounce_interval  # 时间间隔阈值，单位为秒
        self.last_modified = datetime.now()  # 初始化上次修改时间

    def on_modified(self, event):
        if event.src_path == self.filename:
            current_time = datetime.now()
            if (current_time - self.last_modified).total_seconds() > self.debounce_interval:
                self.last_modified = current_time
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
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"json文件中的代码段已更新 - {current_time}")

def monitor_file_changes():
    path = '.'  # 当前目录
    filename = os.path.join(path, 'main.py')
    debounce_interval = 0.5  # 设置防抖动时间间隔为0.5秒
    event_handler = FileMonitorHandler(filename, update_json_file, debounce_interval)
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
