from pypbbot import app, run_server, SimpleDriver

class MyDriver(SimpleDriver):
    async def onPrivateMessage(self, event):
        await self.sendPrivateMsg(event.user_id, 'msg!')

app.default_driver = MyDriver

if __name__ == '__main__':
    run_server(app='example:app', host='localhost', port=8082, reload=True, debug=True)
