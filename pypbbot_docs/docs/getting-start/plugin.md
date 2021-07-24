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

将这段代码保存为.py 文件后，运行它，程序会自动在同级目录下创建以`'plugins'`命名的文件夹，这既是插件目录。

> **注意：** 当`run_server`函数的`reload`参数被设为真值时，框架会开启守护线程，自动监视插件源代码目录的变动情况，并进行重载。在插件目录内创建任意.py 文件，即可创建一个插件。一般情况下，PyPbBot 插件即是一个 Python 模块。

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

直接调用协议层的`Message`类生成消息即繁琐又容易出错，因而 PyPbBot 提供了一个简单的工具类，也即`pypbbot.utils.Clips`类。该类可直接与原生字符串对象或是数值对象混用，也可以用来生成富文本内容。下面是一些具体的例子：

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

> **注意：** 可以被插件使用的事务处理函数优先级一共分为五档，从高到底分别为 VERY_HIGH, HIGH, NORMAL, LOW, VERY_LOW。另外，还存在着高于所有优先级的 SYSTEM 级。一般来说，该优先级不应该被插件使用。

## 主动调用

如果我们需要编写一个能够主动向用户发送消息的机器人，比如说用于整点报时，或是消息推送，那么最基础的方式是调用`pypbbot.server.send_frame`函数。只需构造任意一个`pypbbot.protocol.onebot_api_pb2`的对象（通常以 Req 结尾，如`SendPrivateMsgResp`），就可以直接控制机器人的行为，具体样例如下：

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

> **注意：** `pypbbot.server.drivers`储存了所有客户端 ID 至对应驱动器的映射，如果需要知道有哪些客户端已连入，则可以直接像使用原生字典类型那样调用其`keys`方法。

### 预加载、加载与卸载

插件的加载可以分成两个阶段：预加载与加载。前者类似 Python 的模组导入，后者则是在所有插件加载完成后创建的事务。一般来说，建议在加载而非预加载阶段初始化插件的行为（即使用`onLoading`注册器）。具体样例如下：

```python
from pypbbot.affairs import onLoading, onUnloading

@onLoading() # 插件加载时触发
async def _loading(affair: BaseAffair):
  logger.debug('Counter plugin has been enabled! ')

@onUnloading() # 插件卸载时触发
async def _unloading(affair: BaseAffair):
  logger.debug('Counter plugin has been disabled! ')

```

> **注意：** 跨插件调用不应在预加载阶段进行，因为此时目标插件可能未被载入。

（未完待续）
