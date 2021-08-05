from pypbbot import app, run_server, BaseDriver
from pypbbot.utils import sendBackClipsToAndWait, SingletonType


class SingletonDriver(BaseDriver, metaclass=SingletonType):
    def onPrivateMessage(self, event):
        message = event.raw_message
        if message.startswith('#repr'):
            sendBackClipsToAndWait(event, repr(self))


app.driver_builder = SingletonDriver

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)
