# -*- encoding: utf-8 -*-
__date__ = '2023/06/20 17:37:44'

import os
import socket
import time

import qrcode_terminal
from flask import Flask, render_template, request, send_from_directory
from tqdm import tqdm
from werkzeug.datastructures import FileStorage


class Tools:

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


port = 9000
address = f'http://{Tools.get_local_ip()}:{port}'

app = Flask(__name__)
app.config['UPLOADED_PATH'] = os.path.join(app.root_path, 'upload')
# 最大文件大小:500MB
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for index in tqdm(range(0, len(files))):
            f = files[index]
            print(f'saving file: {f.filename} type: {f.content_type}')
            time.sleep(1)
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html', address=address)


@app.route('/list')
def file_list():
    # 获取当前目录
    current_dir = os.getcwd()

    # 获取当前目录下的所有文件和文件夹
    files = os.listdir(current_dir)

    # 渲染文件列表页面，并传递文件列表数据
    return render_template('file_list.html', files=files)


@app.route('/download/<filename>')
def download(filename):
    # 获取当前目录
    current_dir = os.getcwd()

    # 构造文件路径
    file_path = os.path.join(current_dir, filename)
    print(file_path)
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 使用send_from_directory函数实现文件下载
        return send_from_directory(current_dir, filename, as_attachment=True)
    else:
        # 文件不存在时返回404错误
        return "File not found", 404


if __name__ == '__main__':
    print(f"\033[0;32;40m server address: {address}\033[0m")
    qrcode_terminal.draw(str=address, version=1)
    app.run(host='0.0.0.0', debug=True, port=port)
