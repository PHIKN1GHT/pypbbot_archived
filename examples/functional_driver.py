from pypbbot import app, run_server
from pypbbot.driver import FunctionalDriver
from pypbbot.typing import ProtobufBotEvent as Event
from pypbbot.protocol import PrivateMessageEvent
from pypbbot.utils import Clips, LazyLock
from pypbbot.server import sendPrivateTo

#from asyncio import Lock, get_event_loop
i = 0
iLock = LazyLock()
async def functional_driver(botId: int) -> FunctionalDriver:
    async def onMessage(event: Event):
        if isinstance(event, PrivateMessageEvent):
            global i, iLock
            #if not iLock:
            #    iLock = Lock(loop = get_event_loop())
            with await iLock.try_lock():
                clips = Clips.from_str('The value of i: ') + i
                await sendPrivateTo(botId, event.user_id, clips)
                i += 1

    return onMessage

setattr(app, 'driver_builder', functional_driver)

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)

