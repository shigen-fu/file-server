# -*- encoding: utf-8 -*-
__date__ = "2023/06/20 17:37:44"

import os
import socket
from datetime import datetime

import qrcode_terminal
from flask import Flask, render_template, request, send_from_directory, abort
from termcolor import colored
from typing import List, NoReturn


class Tools:

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    # 格式化文件大小
    @classmethod
    def format_size(cls, size: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    # 格式化时间
    @classmethod
    def format_time(cls, timestamp: int) -> str:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # 获取当前目录下的文件和文件夹列表
    @classmethod
    def get_files_and_dirs(cls, path: str) -> List:
        items = []
        relative_path = path.replace(app.static_folder, "", 1)
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            item_type = "file" if os.path.isfile(item_path) else "dir"
            item_size = (cls.format_size(os.path.getsize(item_path))
                         if os.path.isfile(item_path) else None)
            item_permissions = (oct(os.stat(item_path).st_mode)[-3:]
                                if os.path.isfile(item_path) else None)
            item_create_time = cls.format_time(os.path.getctime(item_path))
            item_modify_time = cls.format_time(os.path.getmtime(item_path))
            items.append({
                "name": item,
                "type": item_type,
                "size": item_size,
                "permissions": item_permissions,
                "create_time": item_create_time,
                "modify_time": item_modify_time,
                "relative_path": relative_path,
            })
        sorted_items = sorted(items,
                              key=lambda x: x["modify_time"],
                              reverse=True)
        return sorted_items


port = 9000
address = f"http://{Tools.get_local_ip()}:{port}"

app = Flask(__name__, static_folder="upload")
upload_path = os.path.join(app.root_path, "upload")
if not os.path.exists(upload_path):
    os.makedirs(upload_path)
app.config["UPLOADED_PATH"] = upload_path
# 最大文件大小:5000MB
max_content_length = 500 * 1024 * 1024 * 10
app.config["MAX_CONTENT_LENGTH"] = max_content_length


# 全局的异常处理器
@app.errorhandler(Exception)
def handle_global_exception(error):
    return str(error), 500


# 请求需要携带特定的参数值
REQUIRED_PARAMS_VALUE = 'xxxx'


@app.before_request
def check_required_params():
    if request.path in ('/', '/list') and request.method == 'GET':
        name_param = request.args.get('name')
        if not name_param or name_param != REQUIRED_PARAMS_VALUE:
            abort(401, 'Invalid request')


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("file")
        for f in files:
            filename = f.filename
            file_path = os.path.join(app.config["UPLOADED_PATH"], filename)
            print(f"Uploading file {filename}")
            with open(file_path, "wb") as file:
                file.write(f.read())
    return render_template("index.html",
                           address=address,
                           max_content_length=max_content_length)


@app.route("/list")
def file_list():
    current_path = os.getcwd()
    files_and_dirs = Tools.get_files_and_dirs(app.static_folder)
    return render_template("file_list.html",
                           address=address,
                           current_path=current_path,
                           files_and_dirs=files_and_dirs)


@app.route("/download/<path:filename>")
def download(filename):
    # 构造文件路径
    file_path = os.path.join(app.static_folder, filename)
    as_attachment_str = request.args.get('as_attachment', default='false')
    as_attachment = True if as_attachment_str.lower() == 'true' else False

    # 检查文件是否存在并且是文件
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # 使用send_from_directory函数实现文件下载
        return send_from_directory(app.static_folder,
                                   filename,
                                   as_attachment=as_attachment)
    else:
        # 文件不存在时返回404错误
        return "File not found", 404


@app.route("/change_dir/<path:pathname>")
def change_dir(pathname):
    current_path = os.path.join(app.static_folder, pathname)
    files_and_dirs = Tools.get_files_and_dirs(current_path)
    return render_template("file_list.html",
                           current_path=current_path,
                           files_and_dirs=files_and_dirs)


def draw_qrcode(address: str) -> NoReturn:
    qrcode_terminal.draw(str=address, version=1)


if __name__ == "__main__":
    print(colored(f"server address: {address}", "red"))
    draw_qrcode(address)
    app.run(host="0.0.0.0", debug=True, port=port)
