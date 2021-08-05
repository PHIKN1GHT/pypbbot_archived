from pypbbot import app, run_server, BaseDriver
from pypbbot.utils import sendBackClipsToAndWait


class SimpleDriver(BaseDriver):
    def onPrivateMessage(self, event):
        message = event.raw_message
        if message.startswith('#echo '):
            sendBackClipsToAndWait(event, message.replace('#echo ', ""))


app.driver_builder = SimpleDriver

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)
