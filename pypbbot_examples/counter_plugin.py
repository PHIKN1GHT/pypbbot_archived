from typing import Awaitable, cast
from pypbbot.affairs.registrar import unfilterable
from pypbbot.affairs import BaseAffair, ChatAffair, onStartsWith, onLoading, onUnloading
from pypbbot.utils import Clips, LazyLock
from pypbbot import logger
import asyncio

i, lock = 0, LazyLock()
akkarin_url = 'https://img.moegirl.org.cn/common/thumb/b/b7/Transparent_Akkarin.jpg/250px-Transparent_Akkarin.jpg'


@onStartsWith('#hello')
async def _(affair: ChatAffair) -> None:
    global i, lock
    with await lock.lock():
        await affair.send('Hello, world! x {}'.format(i))
        await asyncio.sleep(1)
        await affair.send(Clips.from_image_url(akkarin_url) + '\n\阿卡林/\阿卡林/\阿卡林/')
        i += 1


@onStartsWith('#hsync')
def sync_(affair: ChatAffair) -> None:
    global i, lock
    print(i)
    i += 1
    affair.sendAndWait('asd{}'.format(i))


@onLoading()  # 插件加载时触发
async def _loading(affair: BaseAffair) -> None:
    logger.debug('Counter plugin has been enabled! ')


@onUnloading()  # 插件卸载时触发
async def _unloading(affair: BaseAffair) -> None:
    logger.debug('Counter plugin has been disabled! ')
