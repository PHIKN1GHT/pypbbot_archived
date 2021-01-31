from pypbbot import app, run_server, BaseDriver
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent

class SimpleDriver(BaseDriver):
    async def onPrivateMessage(self, event: PrivateMessageEvent):
        if event.raw_message.startswith('#echo '):
            ret = await self.sendPrivateTextMessage(event.user_id, event.raw_message.replace('#echo ', ''))
            print(ret)

    async def onGroupMessage(self, event: GroupMessageEvent):
        if event.raw_message.startswith('#echo '):
            await self.sendGroupTextMessage(event.group_id, event.raw_message.replace('#echo ', ''))

app.default_driver = SimpleDriver

if __name__ == '__main__':
    run_server(app='example:app', host='localhost', port=8082, reload=True, debug=True)
