from pypbbot import app, run_server
from pypbbot.driver import FunctionalDriver
from pypbbot.typing import ProtobufBotEvent as Event
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent
from pypbbot.utils import Clips, LazyLock, sendBackClipsTo
from typing import Union
import asyncio

i, lock = 0, LazyLock()
akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'

async def sayHello(event: Union[PrivateMessageEvent, GroupMessageEvent]):
    if event.raw_message.startswith('#hello'):
        global i
        await sendBackClipsTo(event, 'Hello, world! x {}'.format(i))
        await asyncio.sleep(1)
        await sendBackClipsTo(event,
            Clips.from_image_url(akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
        i += 1

async def functional_driver(botId: int) -> FunctionalDriver: # 函数驱动器（即一个返回处理函数的高阶函数）
    async def onMessage(event: Event) -> None:
        if isinstance(event, PrivateMessageEvent) or isinstance(event, GroupMessageEvent):
            global lock
            with await lock.try_lock():
                await sayHello(event)

    return onMessage

setattr(app, 'driver_builder', functional_driver)

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)
