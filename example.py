from pypbbot import app, run_server, SimpleDriver
from pypbbot.protocol import PrivateMessageEvent 

class MyDriver(SimpleDriver):
    async def onPrivateMessage(self, event: PrivateMessageEvent):
        await self.sendPrivateMsg(event.user_id, 'echo: ' + event.raw_message)

app.default_driver = MyDriver

if __name__ == '__main__':
    run_server(app='example:app', host='localhost', port=8082, reload=True, debug=True)
