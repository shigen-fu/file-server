# -*- encoding: utf-8 -*-
__date__ = '2023/06/20 17:37:44'

import os
import socket
from datetime import datetime

import qrcode_terminal
from flask import Flask, render_template, request, send_from_directory
from termcolor import colored
from tqdm import tqdm
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class Tools:

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    
    
    # 格式化文件大小
    @classmethod
    def format_size(cls, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    # 格式化时间
    @classmethod
    def format_time(cls, timestamp):
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
        
        
    # 获取当前目录下的文件和文件夹列表
    @classmethod
    def get_files_and_dirs(cls, path):
        items = []
        relative_path = path.replace(app.static_folder, "", 1)
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            item_type = 'file' if os.path.isfile(item_path) else 'dir'
            item_size = cls.format_size(os.path.getsize(item_path)) if os.path.isfile(item_path) else None
            item_permissions = oct(os.stat(item_path).st_mode)[-3:] if os.path.isfile(item_path) else None
            item_create_time = cls.format_time(os.path.getctime(item_path))
            item_modify_time = cls.format_time(os.path.getmtime(item_path))
            items.append({'name': item, 'type': item_type, 'size': item_size, 'permissions': item_permissions, 'create_time': item_create_time, 'modify_time': item_modify_time, 'relative_path': relative_path})
        sorted_items = sorted(items, key=lambda x:x['modify_time'], reverse=True)
        return sorted_items


port = 9000
address = f'http://{Tools.get_local_ip()}:{port}'

app = Flask(__name__, static_folder='upload')
app.config['UPLOADED_PATH'] = os.path.join(app.root_path, 'upload')
# 最大文件大小:500MB
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for f in files:
            filename = secure_filename(f.filename)
            file_path = os.path.join(app.config['UPLOADED_PATH'], filename)
            total_size = int(request.headers.get('content-length', 0))
            with open(file_path, 'wb') as file:
                with tqdm(total=total_size, unit='B', unit_scale=True, ncols=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', colour='blue') as pbar:
                    for chunk in f.stream:
                        file.write(chunk)
                        pbar.update(len(chunk))
    return render_template('index.html', address=address)


@app.route('/list')
def file_list():
    current_path = os.getcwd()
    files_and_dirs = Tools.get_files_and_dirs(app.static_folder)
    return render_template('file_list.html', current_path=current_path, files_and_dirs=files_and_dirs)


@app.route('/download/<path:filename>')
def download(filename):
    # 构造文件路径
    file_path = os.path.join(app.static_folder, filename)

    # 检查文件是否存在并且是文件
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # 使用send_from_directory函数实现文件下载
        return send_from_directory(app.static_folder, filename, as_attachment=True)
    else:
        # 文件不存在时返回404错误
        return "File not found", 404

@app.route('/change_dir/<path:pathname>')
def change_dir(pathname):
    current_path = os.path.join(app.static_folder, pathname)
    files_and_dirs = Tools.get_files_and_dirs(current_path)
    return render_template('file_list.html', current_path=current_path, files_and_dirs=files_and_dirs)



if __name__ == '__main__':
    print(colored(f"server address: {address}", "red"))
    qrcode_terminal.draw(str=address, version=1)
    app.run(host='0.0.0.0', debug=True, port=port)
