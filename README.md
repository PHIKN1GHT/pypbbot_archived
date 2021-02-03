# PyProtobufBot

本项目为[ProtobufBot](https://github.com/ProtobufBot/onebot_idl)协议服务端的Python语言实现。

注意，本项目仍处于**早期开发阶段**，请勿用于生产环境。

# 如何使用

首先，运行 `pip install --upgrade pypbbot` 以安装本项目或更新至最新版本。

其次，按照如下方式之一编写机器人程序后，通过调用 `python *_driver.py` 即可运行。（注意把 `*_driver.py` 替换成你的主程序文件的文件名）。

## 类驱动模式

见样例程序源代码： [class_driver.py](https://github.com/PHIKN1GHT/pypbbot/blob/main/examples/class_driver.py)

```python
from pypbbot import app, run_server, BaseDriver
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent
from pypbbot.utils import Clips, LazyLock, sendBackClipsTo
import asyncio

i, lock = 0, LazyLock()
akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'

async def sayHello(event):
    if event.raw_message.startswith('#hello'):
        global i
        await sendBackClipsTo(event, 'Hello, world! x {}'.format(i))
        await asyncio.sleep(1)
        await sendBackClipsTo(event,
            Clips.from_image_url(akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
        i += 1

class SimpleDriver(BaseDriver): # 驱动类
    async def onGroupMessage(self, event: GroupMessageEvent): # 监听的事件类型
        if event.raw_message.startswith('#hello'):
            with await lock.try_lock(): # 加异步锁
                await sayHello(event)

    async def onPrivateMessage(self, event: PrivateMessageEvent):
        if event.raw_message.startswith('#hello'):
            with await lock.try_lock():
                await sayHello(event)

setattr(app, 'driver_builder', SimpleDriver) # 注册驱动器

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)

```

## 函数驱动模式

见样例程序源代码： [functional_driver.py](https://github.com/PHIKN1GHT/pypbbot/blob/main/examples/functional_driver.py)

```python
from pypbbot import app, run_server
from pypbbot.driver import FunctionalDriver
from pypbbot.typing import ProtobufBotEvent as Event
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent
from pypbbot.utils import Clips, LazyLock, sendBackClipsTo
import asyncio

i, lock = 0, LazyLock()
akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'

async def sayHello(event):
    if event.raw_message.startswith('#hello'):
        global i
        await sendBackClipsTo(event, 'Hello, world! x {}'.format(i))
        await asyncio.sleep(1)
        await sendBackClipsTo(event,
            Clips.from_image_url(akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
        i += 1

async def functional_driver(botId: int) -> FunctionalDriver: # 函数驱动器（即一个返回处理函数的高阶函数）
    async def onMessage(event: Event) -> None:
        if isinstance(event, PrivateMessageEvent) or isinstance(event, GroupMessageEvent):
            global lock
            with await lock.try_lock():
                await sayHello(event)

    return onMessage

setattr(app, 'driver_builder', functional_driver)

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)

```

## 事务驱动模式（即插件模式）

见样例程序源代码： [plugin_driver.py](https://github.com/PHIKN1GHT/pypbbot/blob/main/examples/plugin_driver.py) 和样例插件源代码： [plugin_driver.py](https://github.com/PHIKN1GHT/pypbbot/blob/main/examples/plugins/counter_plugin.py) （注意更改插件目录）

```python
from pypbbot import app, run_server
from pypbbot.driver import AffairDriver

setattr(app, 'driver_builder', AffairDriver)
setattr(app, 'plugin_path', 'examples\\plugins')

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)

```

```python
from pypbbot.affairs import BaseAffair, ChatAffair, onStartsWith, onLoading, onUnloading
from pypbbot.utils import Clips, LazyLock
from pypbbot import logger
import asyncio

i, lock = 0, LazyLock()
akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'

@onStartsWith('#hello')
async def _(affair: ChatAffair):
    global i, lock
    with await lock.try_lock():
        await affair.send('Hello, world! x {}'.format(i))
        await asyncio.sleep(1)
        await affair.send(Clips.from_image_url(akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
        i += 1

@onLoading() # 插件加载时触发
async def _loading(affair: BaseAffair):
    logger.debug('Counter plugin has been enabled! ')
    
@onUnloading() # 插件卸载时触发
async def _unloading(affair: BaseAffair):
    logger.debug('Counter plugin has been disabled! ')

```

# 注意事项

## 异步中的同步问题

本框架为异步框架，底层基于 `asyncio` 库实现。默认情况下，框架会为所有从客户端接收到的消息的处理过程**创建一个新的协程**，因而当涉及到某些语句乱序可能会导致不同步的问题时，需要对其进行加同步锁处理。具体加锁方式见例程。

## 关于压力测试

测试用例还在编写，理论上最多支持的客户端数量仅限于使用的缓冲池的大小（默认是65536）。

## 关于文档

在写了……

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

随后，启动协议客户端，它就能够与前文中的 `echobot.py` 例程进行通信。

# 关于开发进度

当前版本仅实现了 `ProtobufBotAPI` 的一个子集。稍后将继续加入更多功能。

- [x] 接收/发送私聊
- [x] 接收/发送群聊
- [ ] 撤销私聊
- [x] 撤销群聊
- [x] 插件化与事务处理
- [x] 日志

