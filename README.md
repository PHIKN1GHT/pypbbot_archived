# PyProtobufBot

Python implementation for [ProtobufBot](https://github.com/ProtobufBot/onebot_idl) Server.

**This project is still WORK IN PROGRESS, DO NOT use for production.**

# How to use

First, you need to `pip install pypbbot`

Second, write your `echobot.py`as above:

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

Finally, start the client and run `python echobot.py` 

Have fun!

# Setting the Client 

Recommended Client: [Go-Mirai-Client](https://github.com/ProtobufBot/Go-Mirai-Client)

Download and compile, then open the client program, edit `application.yml` like above:

```yaml
bot:
  client:
    ws-url: "ws://localhost:8082/ws/test/"
```

Restart the client, Then it should be able to connect to the `echobot.py` in  example.

# Still Work In Progress
Current version has only implemented the little subset of ProtobufBotAPI. More functions are going to be added in future versions.