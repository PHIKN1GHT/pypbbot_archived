### 简介

[PyProtobufBot](https://github.com/PHIKN1GHT/pypbbot)（简称 PyPbBot）是一个使用[Python 语言](https://www.python.org/)实现的，以面向大规模应用为目标的，易于上手与扩展且具有良好效率的[ProtobufBot](https://github.com/ProtobufBot/onebot_idl)协议[服务端](#clientandserver)实现。

<!-- more -->

> **注意：** 尽管 Python 是一门易于上手的编程语言，使用 PyProtobufBot 进行对话式机器人开发仍需要你对相关基本概念有所了解。建议读者在阅读本文档前，熟悉[Python 语言参考手册](https://docs.python.org/zh-cn/3/reference/index.html)中的全部内容。

PyPbBot 是一个以[FastAPI](https://fastapi.tiangolo.com/)为基础的[异步](https://www.ibm.com/developerworks/cn/linux/l-async/)服务端框架，这意味着在源代码的执行过程中，你可以灵活地创建[协程](https://docs.python.org/zh-cn/3/glossary.html#term-coroutine)以提高效率。

（由于协程之间可能会交替执行以提升整体运行效率，这也造成了即使在单线程开发的情况下，你仍需要花点额外的精力注意一下数据的同步问题。）

此外，PyPbBot 内置了一个简单而强大的插件引擎，能够支持以插件化的形式对功能进行渐进式扩展，而且支持热重载。未来，PyPbBot 还将会引入权限控制机制与会话机制，以进一步减轻开发者的抽象负担。

受限于底层实现，PyPbBot 仅支持 Python 3.7 或更高版本。

目前，本项目仍处于早期开发阶段，缺乏文档与测试用例，暂不建议应用于生产环境。

### 安装方法

在确保已经正确安装 Python 3.7 或更高版本后，只需在控制台或终端执行 `pip install --upgrade pypbbot` 即可安装本项目的最新版本。

如果希望体验最新的功能，也可以直接克隆 https://github.com/PHIKN1GHT/pypbbot

### 配置协议客户端

本框架推荐使用的协议客户端: [Go-Mirai-Client](https://github.com/ProtobufBot/Go-Mirai-Client)

首先，下载协议客户端并按照文档对其进行编译，随后在控制台中执行以下代码以设置环境变量：

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

### 快速上手

首先，让我们从一个简单但具有代表性的例程开始：

```python
from pypbbot import app, run_server, BaseDriver
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent
from pypbbot.utils import Clips, LazyLock, sendBackClipsTo
from typing import Union
import asyncio

i, lock = 0, LazyLock()
akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'

async def sayHello(event: Union[PrivateMessageEvent, GroupMessageEvent]):
  global i, lock
  with await lock.try_lock(): # 加异步锁
    await sendBackClipsTo(event, 'Hello, world! x {}'.format(i))
    await asyncio.sleep(1)
    await sendBackClipsTo(event,
    Clips.from_image_url(akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
    i += 1

class SimpleDriver(BaseDriver): # 驱动器类
  async def onPrivateMessage(self, event: PrivateMessageEvent):
    if event.raw_message.startswith('#hello'):
      await sayHello(event)

app.driver_builder = SimpleDriver # 注册驱动器

if __name__ == '__main__':
  run_server(app='__main__:app', host='localhost', port=8082, reload=True)
```

将以上代码保存为.py 后缀的源代码文件，在确保正确安装本项目后执行它（记得也要按上一节的说明启动客户端程序），我们就启动了一个对话式 QQ 机器人。试着通过 QQ 对其发送`#hello`后，它就会回复我们一些文字和图片，其中包含了一个记录着已回复次数的全局变量。

### 发生了什么？

在此例程中，类`SimpleDriver`描述了机器人的全部行为：在收到私聊消息后，对消息文本内容的前缀进行判断，如果前缀以`"#hello"`开头，那么执行异步函数`sayHello`并等待其结束。在`sayHello`函数的执行过程中，协程首先尝试了获取变量`i`的异步锁，也即调用`lock.try_lock`。这一步加锁的过程，确保了不同协程对于`i`的修改过程是原子性的。 _（这也意味着，在处理多个消息时会诞生多个协程。）_

向 PyPbBot 注册[驱动器](#driver)类`SimpleDriver`后，只需要调用`run_server`函数即可启动服务。

这个例程仅展示了使用 PyPbBot 的基本方法之一，也即类驱动器法。相信有经验的读者会发现，这种方法固然清晰直观，却难以胜任项目的扩展。因此，实际开发过程中，建议使用更灵活的事务驱动器法。不过，这需要读者对事务等基本概念有所认知。因此，在开始文档的主体部分前，不妨先了解一下一些基本的概念。
