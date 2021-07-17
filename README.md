# PyProtobufBot

<figure>
  <img src="https://pypbbot.kale1d0.space/assets/logo_large.png" width="256" style="margin:auto"/>
  <h1>Pypbbot</h1>
  <figcaption style="font-style:normal;">一个高效、跨平台、可扩展的<a href="https://github.com/PHIKN1GHT/pypbbot">开源</a> Python QQ 机器人服务端框架。</br>（基于 <a href="https://github.com/ProtobufBot/onebot_idl">
  ProtobufBot</a> 协议）<br/></figcaption>
</figure>
<a href="https://pypbbot.kale1d0.space/">文档主页</a>

注意，本项目仍处于**早期开发阶段**，请勿用于生产环境。

# 如何使用

首先，运行 `pip install --upgrade pypbbot` 以安装本项目或更新至最新版本。

其次，按照如下方式之一编写机器人程序后，通过调用 `python *_driver.py` 即可运行。（注意把 `*_driver.py` 替换成你的主程序文件的文件名）。

## 类驱动模式

见样例程序源代码： [class_driver.py](https://github.com/PHIKN1GHT/pypbbot/blob/main/pypbbot_examples/class_driver.py)

## 函数驱动模式

见样例程序源代码： [functional_driver.py](https://github.com/PHIKN1GHT/pypbbot/blob/main/pypbbot_examples/functional_driver.py)

## 事务驱动模式（即插件模式）

见样例程序源代码： [plugin_driver.py](https://github.com/PHIKN1GHT/pypbbot/blob/main/pypbbot_examples/plugin_driver.py) 和样例插件源代码： [plugin_driver.py](https://github.com/PHIKN1GHT/pypbbot/blob/main/pypbbot_examples/plugins/counter_plugin.py) （注意更改插件目录）

# 注意事项

## 异步中的同步问题

本框架为异步框架，底层基于 `asyncio` 库实现。默认情况下，框架会为所有从客户端接收到的消息的处理过程 **创建一个新的协程** ，因而当涉及到某些语句乱序可能会导致不同步的问题时，需要对其进行加同步锁处理。具体加锁方式见例程。

## 关于压力测试

测试用例还在编写，理论上最多支持的客户端数量仅限于使用的缓冲池的大小（默认是65536）。

# 设置协议客户端 

推荐的协议客户端: [Go-Mirai-Client](https://github.com/ProtobufBot/Go-Mirai-Client)

首先，下载协议客户端并按照文档对其进行编译，随后在控制台中执行以下代码以设置环境变量：

Windows下：

```bat
set UIN=QQ号
set PASSWORD=QQ密码
set WS_URL=ws://localhost:8082/ws/test/
```

Linux下：

```bash
export UIN=QQ号
export PASSWORD=QQ密码
export WS_URL=ws://localhost:8082/ws/test/
```

随后，启动协议客户端，它就能够与前文中的例程进行通信。

# 关于开发进度

当前版本仅实现了 `ProtobufBotAPI` 的一个子集。稍后将继续加入更多功能。

- [x] 接收/发送私聊
- [x] 接收/发送群聊
- [ ] 撤销私聊
- [x] 撤销群聊
- [x] 插件化与事务处理
- [x] 日志

