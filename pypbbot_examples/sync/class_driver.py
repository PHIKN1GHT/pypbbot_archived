from pypbbot import app, run_server, BaseDriver
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent
from pypbbot.utils import Clips, LazyLock, sendBackClipsTo
from typing import Union

i, lock = 0, LazyLock()
akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'


def sayHello(event: Union[PrivateMessageEvent, GroupMessageEvent]):
    if event.raw_message.startswith('#hello'):
        sendBackClipsTo(event, 'Hello, world! x {}'.format(i))
        sendBackClipsTo(event, Clips.from_image_url(
            akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
        i += 1


class SimpleDriver(BaseDriver):  # 驱动类
    def onGroupMessage(self, event: GroupMessageEvent):  # 监听的事件类型
        if event.raw_message.startswith('#hello'):
            sayHello(event)

    def onPrivateMessage(self, event: PrivateMessageEvent):
        if event.raw_message.startswith('#hello'):
            sayHello(event)


setattr(app, 'driver_builder', SimpleDriver)  # 注册驱动器

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)
