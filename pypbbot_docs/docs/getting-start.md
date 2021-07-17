# 新手指南

## 概览

### 简介

　　[PyProtobufBot](https://github.com/PHIKN1GHT/pypbbot)（简称PyPbBot）是一个使用[Python语言](https://www.python.org/)实现的，以面向大规模应用为目标的，易于上手与扩展且具有良好效率的[ProtobufBot](https://github.com/ProtobufBot/onebot_idl)协议[服务端](#clientandserver)实现。
<!-- more -->

>**注意：** 尽管Python是一门易于上手的编程语言，使用PyProtobufBot进行对话式机器人开发仍需要你对相关的基本概念有所了解。建议读者在阅读本文档前，基本了解Python[语言参考手册](https://docs.python.org/zh-cn/3/reference/index.html)中的全部内容。

　　PyPbBot是一个以[FastAPI](https://fastapi.tiangolo.com/)为基础的[异步](https://www.ibm.com/developerworks/cn/linux/l-async/)框架，这意味着在源代码的执行过程中，不同[协程](https://docs.python.org/zh-cn/3/glossary.html#term-coroutine)之间可能会交替执行以提升整体运行效率。但与此同时，这也造成了即使在单线程开发的情况下，你仍需要花点额外的精力注意一下数据的同步问题。

　　此外，PyPbBot内置了一个简单而强大的插件引擎，能够支持以插件化的形式对功能进行渐进式扩展，而且支持热重载。未来，PyPbBot还将会引入权限控制机制与会话机制，以进一步减轻开发者的抽象负担。

　　受限于底层实现，PyPbBot 仅支持 Python 3.7 或更高版本。

　　目前，本项目仍处于早期开发阶段，缺乏文档与测试用例，暂不建议应用于生产环境。

### 安装方法

　　在确保已经正确安装 Python 3.7 或更高版本后，只需在控制台或终端执行 `pip install --upgrade pypbbot` 即可安装本项目的最新版本。

### 配置协议客户端

　　本框架推荐使用的协议客户端: [Go-Mirai-Client](https://github.com/ProtobufBot/Go-Mirai-Client)

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

　　随后，启动协议客户端，按照控制台输出的提示对QQ账户的登陆进行验证，当登陆成功后，它就能够与服务端进行交互。注意，服务端与客户端启动的先后顺序是没有影响的。

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

　　将以上代码保存为.py后缀的源代码文件，在确保正确安装本项目后执行它（记得也要按上一节的说明启动客户端程序），我们就启动了一个对话式QQ机器人。试着通过QQ对其发送`#hello`后，它就会回复我们一些文字和图片，其中包含了一个记录着已回复次数的全局变量。

### 发生了什么？

　　在此例程中，类`SimpleDriver`描述了机器人的全部行为：在收到私聊消息后，对消息文本内容的前缀进行判断，如果前缀以`"#hello"`开头，那么执行异步函数`sayHello`并等待其结束。在`sayHello`函数的执行过程中，协程首先尝试了获取变量`i`的异步锁，也即调用`lock.try_lock`。这一步加锁的过程，确保了不同协程对于`i`的修改过程是原子性的。 *（这也意味着，在处理多个消息时会诞生多个协程。）* 

　　向PyPbBot注册[驱动器](#driver)类`SimpleDriver`后，只需要调用`run_server`函数即可启动服务。

　　这个例程仅展示了使用PyPbBot的基本方法之一，也即类驱动器法。相信有经验的读者会发现，这种方法固然清晰直观，却难以胜任项目的扩展。因此，实际开发过程中，建议使用更灵活的事务驱动器法。不过，这需要读者对事务等基本概念有所认知。因此，在开始文档的主体部分前，不妨先了解一下一些基本的概念。

## 基本概念

### 客户端与服务端

　　在早期的QQ机器人开发技术中，许多框架曾采用类似酷Q（CoolQ）的设计方案，也即 **使用一个支持插件化的机器人程序来登录某一特定QQ账户以提供服务** 。这种设计方案固然清晰直观，但当需要通过大量QQ账户来提供统一的服务时，其弊端就显露了出来： **插件的编写者将不得不自行处理进程间的同步与数据通信等问题，而这类工作对于编程初学者来说往往繁琐易错** *（对于某些经验丰富的开发者来说亦是如此）*。因而，另一批以[NoneBot](https://github.com/nonebot/nonebot)、[ProtobufBot](https://github.com/ProtobufBot/onebot_idl)等为主的框架则采取了相反的设计思路试图解决这个问题： **由支持插件化的框架本身作为服务端，来与多个登陆了某一特定QQ账户的客户端程序进行通信** ，从而简化了许多原本需要插件编写者进行处理的繁琐工作。这一思路的转变， **极大降低了插件开发者们编写大规模服务程序的难度，也有效提升了整个系统的可扩展性与可维护性** 。本框架亦采用了这样的设计方法。

　　也即是说，在本文以及所有[ProtobufBot](https://github.com/ProtobufBot/onebot_idl)相关的所有文档中，我们把 **仅仅实现了QQ的消息收发等协议层功能的程序** 称为机器人的 **客户端（Client）** ，而把 **负责处理业务逻辑的程序** 称为机器人的 **服务端（Server）** 。

### 应用程序编程接口、事件与消息

　　在本文（以及[PyProtobufBot文档](https://github.com/PHIKN1GHT/pypbbot)）中，如若不加说明， **应用程序编程接口（API）** 、 **事件（Event）** 与 **消息（Message）** 的定义皆来自于 **协议层** （也即[ProtobufBot](https://github.com/ProtobufBot/onebot_idl)）。简单的说，在协议层一共具有两大类协议，其一是类似于[远程过程调用（RPC）](https://en.wikipedia.org/wiki/Remote_procedure_call)的协议，通常用于 **让服务端向客户端发出请求** ，且发出后 **都会收到来自客户端的响应** 以确认请求被成功执行，比如发送私聊或是群聊消息，这一类协议被称为 **应用程序编程接口（API）** ；而另一类协议用于 **让服务端能够被动接受来自于客户端的消息** ，比如当收到私聊消息或好友请求时能够对其进行处理，这一类协议被称为 **事件（Event）** 。 **消息（Message）** 则是一种协议层上的复合数据结构，其 **描述了一段或多段QQ消息的内容**（除了文本消息外，还支持图片、语音等[富文本格式](https://en.wikipedia.org/wiki/Rich_Text_Format)）。协议层除了以上三种结构外，还有另一种 **用于数据封装** 的 **数据帧（Frame）** 结构，不过这一结构对于插件开发者是透明的，一般不用考虑。

> **注意：** 一般情况下，我们认为事件是一个 **只读** 的数据合集。

　　在使用PyPbBot开发的过程中，既可以直接对以上三种结构进行操作，也可以使用PyPbBot提供的简单封装。相对来说，后者更加简洁易用。

　　以上结构定义于源代码的`pypbbot.protocol`与`pypbbot.typing`包中。

<h2 id="driver"> 驱动器</h2>

　　**驱动器（Driver）** 是本框架的核心概念之一，其含义是指 **负责与客户端进行交互的对象** 。注意，这里的对象即可以是面向对象编程中的术语，也 **可以是一个高阶函数** 。默认情况下，PyPbBot会 **为每个客户端创建一个驱动器对象，并为每个事件启创建一个新的协程** 。

> **注意：** 当需要使用唯一全局驱动器时，一般推荐使用高阶函数，或着使用单例模式（即修改类的定义为`class AffairDriver(BaseDriver, metaclass=SingletonType)`，其中`SingletonType`位于`pypbbot.typing`模块内)。如果需要对驱动器的构造行为进行灵活的限制或处理，则只需重载 `__new__` 函数即可。

### 事务、过滤器与处理程序

　　前文中，我们有提到事件应该是一个状态不可变的结构。但是在处理事件的过程中，我们常常会希望能够 **将某些操作或者可变的状态与不可变的事件进行绑定，以方便对事件进行阶段化的、模块化的处理** 。 **事务（Affair）** 正是这一目的的体现。事务即是事件的封装，通常来说事务以事件为基础，且其生命周期通常会略长于事件。

　　 **事务处理程序（Handler）** 则是 **用于处理事务的函数** 。一般来说，事务处理程序需要与某个 **事务过滤器（Filter）** 绑定。当过滤器对事务返回真值时，表明该事务可被事务处理程序处理。而且，事务处理程序具有优先级。优先级越高，则事务处理程序会更早的接收到这个事务。

## 插件化开发

　　插件化开发，也即 **使用事务引擎** 进行开发，是面向大规模应用的基础。相比类驱动器或高阶函数驱动器模式，这种方法更加简便灵活，易于扩展。

### 使用插件驱动器

　　使用插件化开发的第一步，是将默认的驱动器更换为插件驱动器，也即编写以下代码：

```python
from pypbbot import app, run_server
from pypbbot.driver import AffairDriver

app.driver_builder = AffairDriver
app.plugin_path = 'plugins'

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)
```

　　将这段代码保存为.py文件后，运行它，程序会自动在同级目录下创建以`'plugins'`命名的文件夹，这既是插件目录。

> **注意：** 当`run_server`函数的`reload`参数被设为真值时，框架会开启守护线程，自动监视插件源代码目录的变动情况，并进行重载。在插件目录内创建任意.py文件，即可创建一个插件。一般情况下，PyPbBot插件即是一个Python模块。

### 注册事务处理程序

　　通过使用注册函数`onStartsWith`，我们可以轻易编写出与前文例程具有相同功能的插件。该注册函数会将特定的事务处理器（即本例程中的`say_hello`函数）与内置的消息前缀检查过滤器所绑定，因而当机器人收到符合条件的消息（也即以`#hello`作为前缀的消息，无论群聊或私聊）

```python
from pypbbot.affairs import BaseAffair, ChatAffair, onStartsWith
from pypbbot.utils import Clips, LazyLock
from pypbbot import logger
import asyncio

i, lock = 0, LazyLock()
akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'

@onStartsWith('#hello')
async def say_hello(affair: ChatAffair):
    global i, lock
    with await lock.try_lock():
        await affair.send('Hello, world! x {}'.format(i))
        await asyncio.sleep(1)
        await affair.send(Clips.from_image_url(akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
        i += 1
```

　　常用的注册函数还包括`unfilterable`（捕获任意事务），`onMessage`(捕获任意消息事务)，`onEndsWith`(捕获任意消息事务并检查后缀），`onPrivateMessage`(捕获任意私聊消息事务)，`onGroupMessage`(捕获任意私聊群聊事务)


### 消息生成

　　直接调用协议层的`Message`类生成消息即繁琐又容易出错，因而PyPbBot提供了一个简单的工具类，也即`pypbbot.utils.Clips`类。该类可直接与原生字符串对象或是数值对象混用，也可以用来生成富文本内容。下面是一些具体的例子：

```python
from pypbbot.utils import Clips

def test_clips_add():
    a = Clips.from_str('aA')
    b = Clips.from_str('bB')
    assert str(a + b) == 'aAbB'
    assert str(123 + b) == '123bB'
    assert str(b + 0.0) == 'bB0.0'
    assert str('str' + a) == 'straA'
    a = Clips.from_image_url(akkarin_url) + 'asd'
    msglst = a.toMessageList() # 生成消息序列，可以直接用于协议层对象。
```


### 指定优先级

　　尽管事务本身并不具有优先级，我们可以为事务处理程序指定优先级。高优先级的事务处理程序将会被优先调用。指定优先级的方式也很简单，只需在文件头部加入`from pypbbot.affairs import HandlerPriority`，随后为注册函数增加参数，比如说将上例对应行`@onStartsWith('#hello', priority = HandlerPriority.HIGH)`即可。

>**注意：** 可以被插件使用的事务处理函数优先级一共分为五档，从高到底分别为VERY_HIGH, HIGH, NORMAL, LOW, VERY_LOW。另外，还存在着高于所有优先级的SYSTEM级。一般来说，该优先级不应该被插件使用。

## 主动调用

　　如果我们需要编写一个能够主动向用户发送消息的机器人，比如说用于整点报时，或是消息推送，那么最基础的方式是调用`pypbbot.server.send_frame`函数。只需构造任意一个`pypbbot.protocol.onebot_api_pb2`的对象（通常以Req结尾，如`SendPrivateMsgResp`），就可以直接控制机器人的行为，具体样例如下：

```python
from pypbbot.protocol import SendPrivateMsgReq, PrivateMessageEvent, GroupMessageEvent, SendGroupMsgReq
async def sendBackClipsTo(event: Union[GroupMessageEvent, PrivateMessageEvent], clips: Union[Clips, str, int, float]):
  clips = Clips() + clips
  api_content: Optional[Union[SendPrivateMsgReq, SendGroupMsgReq]] = None
  if isinstance(event, PrivateMessageEvent):
    api_content = SendPrivateMsgReq()
    api_content.user_id, auto_escape = event.user_id, True
  elif isinstance(event, GroupMessageEvent):
    api_content = SendGroupMsgReq()
    api_content.group_id, auto_escape = event.group_id, True
  api_content.message.extend(clips.toMessageList())
  return await pypbbot.server.send_frame(event.self_id, api_content)
```

>**注意：** `pypbbot.server.drivers`储存了所有客户端ID至对应驱动器的映射，如果需要知道有哪些客户端已连入，则可以直接像使用原生字典类型那样调用其`keys`方法。

### 预加载、加载与卸载

　　插件的加载可以分成两个阶段：预加载与加载。前者类似Python的模组导入，后者则是在所有插件加载完成后创建的事务。一般来说，建议在加载而非预加载阶段初始化插件的行为（即使用`onLoading`注册器）。具体样例如下：

```python
from pypbbot.affairs import onLoading, onUnloading

@onLoading() # 插件加载时触发
async def _loading(affair: BaseAffair):
  logger.debug('Counter plugin has been enabled! ')
    
@onUnloading() # 插件卸载时触发
async def _unloading(affair: BaseAffair):
  logger.debug('Counter plugin has been disabled! ')

```

>**注意：** 跨插件调用不应在预加载阶段进行，因为此时目标插件可能未被载入。

（未完待续）
