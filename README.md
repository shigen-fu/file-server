<h1 align="center">file-server(开源的局域网文件共享工具)</h1>

<div align="center">

[English](./README.en.md) | [简体中文](./README.md)
🗂「file-server」是一个开箱即用的局域网文件共享工具，扫码即可上传文件，点击即可下载文件

[![GitHub license](https://img.shields.io/github/license/shigen-fu/file-server?style=flat-square)](LICENSE)
[![Release Version](https://img.shields.io/github/v/release/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/releases/latest)
[![GitHub Star](https://img.shields.io/github/stars/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/stargazers)
[![GitHub Fork](https://img.shields.io/github/forks/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/network/members)
[![GitHub issues](https://img.shields.io/github/issues/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/shigen-fu/file-server?style=flat-square)](https://github.com/shigen-fu/file-server/issues?q=is%3Aissue+is%3Aclosed)

![GitHub Repo size](https://img.shields.io/github/repo-size/shigen-fu/file-server?style=flat-square&color=3cb371)

<br>
</div>

# 🧑‍💻file-server介绍

一款开源的局域网文件传输共享工具，如果使用的是移动设备，直接扫描终端中的二维码或者浏览器页面上的二维码即可上传文件。</br>
上传完毕之后的文件将会以列表的形式展示文件的具体信息：如文件名、大小、权限、修改时间等信息，单击【下载】按钮即可下载文件到设备中。</br>

具体的使用可参考 `shigen` 的文章：[开源一个局域网文件共享工具](https://juejin.cn/post/7304268951298392114)

# 🛠项目依赖

需要有python3+的环境

* 后端依赖
  + Flask
  + qrcode_terminal
  + termcolor

> 更多信息可参考[requirements.txt](./requirements.txt)文件

* 前端依赖
  + dropzone
  + qrcodejs
  + bootstrap

> 依赖全部以CDN的形式引入，可以实现免安装，开箱即用

# 📇仓库地址

[file-server 一款开箱即用的局域网文件共享工具](https://github.com/shigen-fu/file-server.git)

# 📋功能清单

## 核心功能
- **文件上传**: 支持拖拽上传、扫码上传、多文件上传
- **文件下载**: 一键下载文件到本地设备
- **文件管理**: 文件列表展示、文件删除、文件夹创建
- **二维码分享**: 自动生成文件下载二维码和上传二维码

## 高级功能
- **用户认证**: 支持多用户登录和权限管理
- **文件统计**: 实时统计文件类型占比和文件夹存储排行
- **配置管理**: 灵活的配置文件系统，支持运行时配置修改
- **会话管理**: 安全的会话机制，支持自动过期
- **仪表板**: 可视化统计信息展示

## 技术特性
- **跨平台**: 支持Windows、macOS、Linux系统
- **容器化**: 提供Docker支持，一键部署
- **轻量级**: 前端依赖全部CDN引入，无需额外安装
- **高性能**: 基于Flask框架，响应快速

# 🟢如何使用

只需要一条命令即可运行

```shell
git clone https://github.com/shigen-fu/file-server.git && cd file-server && pip install -r requirements.txt && python app.py
```

## Dockerfile

`shigen` 一直用的是mac，所以没有发现问题。最后移植到了windows平台，发现运行项目，flask都有问题。于是新增了Dockerfile，直接在docker容器中运行服务。以下是相关命令：

```shell
docker build -t file-server:1.0.0 .
docker run -d -p 9000:9000 --name file-server -v $(pwd)/file:/app/upload file-server:1.0.0
```

> docker初次构建的时间可能会很长，因为python官方的docker镜像大约在1GB左右。大部分的时间都在拉取镜像，建议配置docker的镜像加速。

可以先提前单独下载好需要用到的基础镜像：

```shell
docker pull python:3.9
```

### 24-4-25新增部署方式

如果觉得上述的命令敲起来麻烦，可以直接运行给定的部署脚本。

```shell
bash deploy.sh
```
