# 安装与使用

## 安装PyPbBot

在确保已经正确安装 Python 3.7 或更高版本后，只需在控制台或终端执行 `pip install --upgrade pypbbot` 即可安装本项目的最新版本。

如果希望体验处于开发中的功能，也可以直接克隆[本项目](https://github.com/PHIKN1GHT/pypbbot)的源码，并在项目根目录内进行开发。

## 配置协议客户端

本框架需要配合协议客户端（稍后会具体解释）使用。推荐的协议客户端: [Go-Mirai-Client](https://github.com/ProtobufBot/Go-Mirai-Client)

首先，下载协议客户端并按照文档对其进行编译（或是在其发布页面下载预编译的二进制可执行文件），随后在控制台中执行以下代码以设置环境变量：

Windows 下：

```bat
set UIN=QQ号
set PASSWORD=QQ密码
set WS_URL=ws://localhost:8082/ws/test/
```

Linux 下：

```bash
export UIN=QQ号
export PASSWORD=QQ密码
export WS_URL=ws://localhost:8082/ws/test/
```

随后，启动协议客户端，按照控制台输出的提示对 QQ 账户的登陆进行验证，当登陆成功后，它就能够与服务端进行交互。注意，服务端与客户端启动的先后顺序是没有影响的。

## 启动程序

两个方法：编写主程序，通过模块调用启动

pythom -m pypbbot.serve -h host -p 8082 -wsaddr /ws/test/ -qsize 400

alias pbpbbot='pythom -m pypbbot.serve'
pythom -m pypbbot.serve

.env文件，
