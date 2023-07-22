# -*- encoding: utf-8 -*-
__date__ = '2023/06/20 17:37:44'

import os
import socket
import time

import qrcode_terminal
from flask import (Flask, redirect, render_template, request,
                   send_from_directory)
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

class FileStorageWithProgress:
    def __init__(self, file, total):
        self.file = file
        self.total = total
        self.progress_bar = tqdm(total=total, unit='B', unit_scale=True)
    
    def write(self, data):
        self.file.write(data)
        self.progress_bar.update(len(data))
    
    def flush(self):
        self.file.flush()
    
    def close(self):
        self.file.close()
        self.progress_bar.close()


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
            with open(file_path, 'wb') as file:
                file_storage = FileStorageWithProgress(
                    file,
                    int(request.headers.get('content-length', 0))
                )
                f.save(file_storage)
    return render_template('index.html', address=address)


@app.route('/list')
def file_list():
    # 获取当前目录
    current_dir = app.static_folder

    # 获取当前目录下的所有文件和目录
    files_and_dirs = []

    for file_or_dir in os.listdir(current_dir):
        file_or_dir_path = os.path.join(current_dir, file_or_dir)
        # 判断是文件还是目录
        if os.path.isdir(file_or_dir_path):
            files_and_dirs.append({'name': file_or_dir, 'type': 'dir'})
        else:
            files_and_dirs.append({'name': file_or_dir, 'type': 'file'})
    # 渲染模板，显示文件列表和目录切换链接
    return render_template('file_list.html', files_and_dirs=files_and_dirs)


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
    # 切换目录
    os.chdir(pathname)
    
    # 重定向到根目录
    return redirect('/list')



if __name__ == '__main__':
    print(colored(f"server address: {address}", "red"))
    qrcode_terminal.draw(str=address, version=1)
    app.run(host='0.0.0.0', debug=True, port=port)
