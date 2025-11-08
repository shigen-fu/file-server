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

# 📋Feature List

## Core Features
- **File Upload**: Support drag-and-drop upload, QR code upload, multiple file upload
- **File Download**: One-click download files to local device
- **File Management**: File list display, file deletion, folder creation
- **QR Code Sharing**: Automatically generate download and upload QR codes

## Advanced Features
- **User Authentication**: Support multi-user login and permission management
- **File Statistics**: Real-time statistics on file type distribution and folder storage ranking
- **Configuration Management**: Flexible configuration system with runtime modification support
- **Session Management**: Secure session mechanism with automatic expiration
- **Dashboard**: Visual statistical information display

## Technical Features
- **Cross-Platform**: Support for Windows, macOS, and Linux systems
- **Containerization**: Docker support with one-click deployment
- **Lightweight**: All frontend dependencies loaded via CDN, no additional installation required
- **High Performance**: Built on Flask framework with fast response times

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
