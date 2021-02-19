from pypbbot import app, run_server, BaseDriver
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent
from pypbbot.utils import Clips, AsyncLock, sendBackClipsTo
from typing import Union
import asyncio

i, lock = 0, AsyncLock()
akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'

async def sayHello(event: Union[PrivateMessageEvent, GroupMessageEvent]):
    if event.raw_message.startswith('#hello'):
        global i
        await sendBackClipsTo(event, 'Hello, world! x {}'.format(i))
        await asyncio.sleep(1)
        await sendBackClipsTo(event,
            Clips.from_image_url(akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
        i += 1

class SimpleDriver(BaseDriver): # 驱动类
    async def onGroupMessage(self, event: GroupMessageEvent): # 监听的事件类型
        if event.raw_message.startswith('#hello'):
            with await lock.lock(): # 加异步锁
                await sayHello(event)

    async def onPrivateMessage(self, event: PrivateMessageEvent):
        if event.raw_message.startswith('#hello'):
            with await lock.lock():
                await sayHello(event)

setattr(app, 'driver_builder', SimpleDriver) # 注册驱动器

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)
