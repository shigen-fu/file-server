# -*- encoding: utf-8 -*-
__date__ = '2023/06/20 17:37:44'

import os
import socket

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
    
    @staticmethod
    # 获取当前目录下的文件和文件夹列表
    def get_files_and_dirs(path):
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            item_type = 'file' if os.path.isfile(item_path) else 'dir'
            items.append({'name': item, 'type': item_type})
        return items


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
    files_and_dirs = Tools.get_files_and_dirs(current_path)
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
    current_path = os.path.join(os.getcwd(), pathname)
    files_and_dirs = Tools.get_files_and_dirs(current_path)
    return render_template('file_list.html', current_path=current_path, files_and_dirs=files_and_dirs)



if __name__ == '__main__':
    print(colored(f"server address: {address}", "red"))
    qrcode_terminal.draw(str=address, version=1)
    app.run(host='0.0.0.0', debug=True, port=port)
