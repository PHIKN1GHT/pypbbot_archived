from pypbbot import app, run_server, BaseDriver
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent
from pypbbot.utils import Clips
from pypbbot.log import logger

from typing import Union
import asyncio

akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'
class SimpleDriver(BaseDriver):
    async def sayHello(self, event: Union[GroupMessageEvent, PrivateMessageEvent]):
        logger.info('Say hello!')
        resp = await self.sendBackClips(event, 'Hello, world!')
        await asyncio.sleep(1)
        await self.sendBackClips(event, 3)
        await asyncio.sleep(1)
        await self.sendBackClips(event, 2)
        await asyncio.sleep(1)
        await self.sendBackClips(event, 1.111)
        await asyncio.sleep(1)
        await self.sendBackClips(event, 
            Clips.from_image_url(akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
        await asyncio.sleep(3)
        
        await self.recallMessage(resp.message_id)


    async def onGroupMessage(self, event: GroupMessageEvent):
        if event.raw_message.startswith('#hello'):
            await self.sayHello(event)

    async def onPrivateMessage(self, event: PrivateMessageEvent):
        if event.raw_message.startswith('#hello'):
            await self.sayHello(event)

from pypbbot.driver import AffairDriver
setattr(app, 'default_driver', AffairDriver)

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)

