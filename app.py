# -*- encoding: utf-8 -*-
__date__ = '2023/06/20 17:37:44'

import os
import socket
import time

import qrcode_terminal
from flask import Flask, render_template, request
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


if __name__ == '__main__':
    print(f"\033[0;32;40m server address: {address}\033[0m")
    qrcode_terminal.draw(str=address, version=1)
    app.run(host='0.0.0.0', debug=True, port=port)
