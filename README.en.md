<h1 align="center">file-server(Open source LAN file sharing tool)</h1>

<div align="center">

[English](./README.en.md) | [简体中文](./README.md)
🗂「file-server」A plug-and-play LAN file sharing tool, scan to upload files, click to download files.

[![GitHub license](https://img.shields.io/github/license/shigen-fu/file-server?style=flat-square)](LICENSE)
[![Release Version](https://img.shields.io/github/v/release/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/releases/latest)
[![GitHub Star](https://img.shields.io/github/stars/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/stargazers)
[![GitHub Fork](https://img.shields.io/github/forks/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/network/members)
[![GitHub issues](https://img.shields.io/github/issues/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/issues?q=is%3Aissue+is%3Aclosed)

![GitHub Repo size](https://img.shields.io/github/repo-size/shigen-fu/file-server?style=flat-square&color=3cb371)

<br>
</div>

# 🧑‍💻file-server introduction

A open-source LAN file transfer and sharing tool, if using a mobile device, simply scan the QR code on the terminal or the QR code on the browser page to upload files. After uploading, the files will be displayed in a list format with detailed information such as file name, size, permissions, modification time, etc. Click the [Download] button to download the file to your device.

For specific usage, you can refer to the article by `shigen` : [Open Source a LAN File Sharing Tool](https://juejin.cn/post/7304268951298392114).

# 🛠project dependencies

need python3+ environment

* dependencies of backend
  + Flask
  + qrcode_terminal
  + termcolor

> more info can refer the file [requirements.txt](./requirements.txt)

* dependencies of frontend
  + dropzone
  + qrcodejs
  + bootstrap

> All dependencies are introduced in the form of CDN, allowing for a hassle-free installation and immediate use.

# 📇git repository

[file-server An open source LAN file sharing tool](https://github.com/shigen-fu/file-server.git)

# 🟢how to use

Just one command.

```shell
git clone https://github.com/shigen-fu/file-server.git && cd file-server && pip install -r requirements.txt && python app.py
```

## Dockerfile

`shigen` has been using macOS all along, so I didn't notice any issues. Finally, when he ported the project to the Windows platform, I encountered problems running Flask. Therefore, I added a Dockerfile to run the service directly in a Docker container. Below are the relevant commands:

```shell
docker build -t file-server:1.0.0 .
docker run -d -p 9000:9000 --name file-server -v $(pwd)/file:/app/upload file-server:1.0.0
```

> The initial build of Docker may take a long time because the official Python Docker image is around 1GB in size. Most of the time is spent pulling the image, so it's recommended to configure Docker with image acceleration.

You can first separately download the base image needed:

```shell
docker pull python:3.9
```

### Deployment Method Added on 24-4-25

If you find the above commands cumbersome to type, you can directly run the provided deployment script.

```shell
bash deploy.sh
```

## Deployment IDE and adviced plugins

IDE: Visual Studio Code

advanced plugins

| Serial No. | Plugin Name                                 | Description                                                                                                               | Installation Command                                 |
| ---------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 1          | Python Docstring Generator                  | Automatically generates Docstring for Python functions and classes, supports multiple formats (e.g. Google, NumPy, etc.). | ext install njpwerner.autodocstring                  |
| 2          | Python Indent                               | Improves the indentation of Python code, making it more intelligent.                                                      | ext install kevinrose.vsc-python-indent              |
| 3          | Python Test Explorer for Visual Studio Code | Provides a test resource explorer for running and debugging Python unit tests in VSCode.                                  | ext install littlefoxteam.vscode-python-test-adapter |
| 4          | MagicPython                                 | Enhances syntax highlighting for Python code, particularly when using modern Python features.                             | ext install magicstack.magicpython                   |
| 5          | Python Snippets                             | Provides some commonly used Python code snippets to enhance development efficiency.                                       | ext install frhtylcn.pythonsnippets                  |
| 6          | Black Formatter                             | Black is a Python code formatting tool that automatically reformats code to comply with PEP 8 standards.                  | ext install ms-python.black-formatter                |
| 7          | isort                                       | Automatically sorts Python import statements to make the code more orderly.                                               | ext install ms-python.isort                          |

