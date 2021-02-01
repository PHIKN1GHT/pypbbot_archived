# PyProtobufBot

本项目为[ProtobufBot](https://github.com/ProtobufBot/onebot_idl)协议服务端的Python语言实现。

注意，本项目仍处于**早期开发阶段**，请勿用于生产环境。

# 如何使用

首先，运行 `pip install --upgrade pypbbot` 以安装本项目或更新至最新版本。

其次，按照如下方式编写代码文件 `echobot.py` ：

``` python
from pypbbot import app, run_server, BaseDriver
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent

class SimpleDriver(BaseDriver):
    async def onPrivateMessage(self, event: PrivateMessageEvent):
        if event.raw_message.startswith('#echo '):
            await self.sendPrivateTextMessage(event.user_id, event.raw_message.replace('#echo ', ''))

    async def onGroupMessage(self, event: GroupMessageEvent):
        if event.raw_message.startswith('#echo '):
            await self.sendGroupTextMessage(event.group_id, event.raw_message.replace('#echo ', ''))

app.default_driver = SimpleDriver

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True, debug=True)
```

最后，启动协议客户端并运行 `python echobot.py` 。

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

当前版本仅实现了`ProtobufBotAPI`的一个子集（发送私聊和群聊消息）。稍后将继续加入更多功能。

- [x] 接收/发送私聊
- [x] 接收/发送群聊
- [ ] 撤销私聊
- [x] 撤销群聊

