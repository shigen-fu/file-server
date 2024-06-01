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

## 开发IDE及插件推荐

开发IDE：Visual Studio Code

插件推荐：

| 序号 | 插件名称                                    | 描述                                                                     | 安装命令                                             |
| ---- | ------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------- |
| 1    | Python Docstring Generator                  | 自动生成Python函数和类的Docstring，支持多种格式（如Google、NumPy等）。   | ext install njpwerner.autodocstring                  |
| 2    | Python Indent                               | 改进Python代码的缩进，使其更加智能。                                     | ext install kevinrose.vsc-python-indent              |
| 3    | Python Test Explorer for Visual Studio Code | 提供了一个测试资源管理器，可以在VSCode中运行和调试Python单元测试。       | ext install littlefoxteam.vscode-python-test-adapter |
| 4    | MagicPython                                 | 增强Python代码的语法高亮，特别是在使用现代Python特性时表现更好。         | ext install magicstack.magicpython                   |
| 5    | Python Snippets                             | 提供了一些常用的Python代码片段，提升开发效率。                           | ext install frhtylcn.pythonsnippets                  |
| 6    | Black Formatter                             | Black是一个Python代码格式化工具，可以自动格式化代码，使其符合PEP 8规范。 | ext install ms-python.black-formatter                |
| 7    | isort                                       | 自动排序Python导入语句，使代码更加整洁。                                 | ext install ms-python.isort                          |