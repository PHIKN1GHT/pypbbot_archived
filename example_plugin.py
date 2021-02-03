from pypbbot import app, AffairDriver, load_plugins, run_server
from pypbbot.plugin import _handle, _handlers
from pypbbot.affairs import BaseAffair

setattr(app, 'driver_builder', AffairDriver)
setattr(app, 'plugin_path', 'plugins')
if __name__ == '__main__':
    #load_plugins()
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)
    #print(_handlers)
    #run_server(app='__main__:app', host='localhost', port=8082, reload=True, debug=True)

    #from pypbbot.plugin import BaseAffair, _handle, _handlers, load_plugins
    #aff = BaseAffair()
    #aff.msg = 'asd'
    #print(123)
    
    #_handle(aff)

#    run_server(app='__main__:app', host='localhost', port=8082, reload=True, debug=True)

'''

akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'
class SimpleDriver(BaseDriver):
    async def sayHello(self, event: Union[GroupMessageEvent, PrivateMessageEvent]):
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
        print(resp.message_id)
        await self.recallMessage(resp.message_id)


    async def onGroupMessage(self, event: GroupMessageEvent):
        if event.raw_message.startswith('#hello'):
            await self.sayHello(event)

    async def onPrivateMessage(self, event: PrivateMessageEvent):
        if event.raw_message.startswith('#hello'):
            await self.sayHello(event)

setattr(app, 'driver_builder', SimpleDriver)
'''
