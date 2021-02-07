from enum import Enum
from typing import Optional, Union
import pypbbot
from pypbbot.typing import ProtobufBotEvent
from pypbbot.logging import logger
from pypbbot.driver import BaseDriver
from pypbbot.utils import sendBackClipsTo, Clips

class HandlerPriority(Enum):
    SYSTEM = 0 # SHOULD NOT USED BY PLUGINS
    VERY_HIGH = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    VERY_LOW = 5

    def __lt__(self, other):
        return self.value < other.value

class BaseAffair:
    def __init__(self, driver, event):
        logger.debug('A new affair has been created for event [{}]'.format(type(event)))
        self.event = event
        self.driver = driver
        self.finished = False

class ChatAffair(BaseAffair):
    def __init__(self, driver, event, sender_id):
        super().__init__(driver, event)
        self.receiver_id = event.self_id
        self.sender_id = sender_id
        self.raw_message = event.raw_message

    async def send(self, clips: Union[Clips, str, int, float]):
        await sendBackClipsTo(self.event, clips)



def unfilterable(priority: HandlerPriority = HandlerPriority.NORMAL):
    def _unfilterable_filter(_: BaseAffair) -> bool:
        return True
    return pypbbot.plugin.onFilter(_unfilterable_filter, priority)

def onMessage(priority: HandlerPriority = HandlerPriority.NORMAL):
    def _message_filter(_: BaseAffair) -> bool:
        return isinstance(_, ChatAffair)
    return pypbbot.plugin.onFilter(_message_filter, priority)

from pypbbot.protocol import PrivateMessageEvent
def onPrivateMessage(priority: HandlerPriority = HandlerPriority.NORMAL):
    def _private_message_filter(_: BaseAffair) -> bool:
        return isinstance(_.event, PrivateMessageEvent)
    return pypbbot.plugin.onFilter(_private_message_filter, priority)

from pypbbot.protocol import GroupMessageEvent
def onGroupMessage(priority: HandlerPriority = HandlerPriority.NORMAL):
    def _group_message_filter(_: BaseAffair) -> bool:
        return isinstance(_.event, GroupMessageEvent)
    return pypbbot.plugin.onFilter(_group_message_filter, priority)

def onStartsWith(prefix: str, priority: HandlerPriority = HandlerPriority.NORMAL):
    def _on_starts_with_filter(_: BaseAffair) -> bool:
        return (isinstance(_, ChatAffair)) and (_.event.raw_message.startswith(prefix))
    return pypbbot.plugin.onFilter(_on_starts_with_filter, priority)

def onEndsWith(suffix: str, priority: HandlerPriority = HandlerPriority.NORMAL):
    def _on_ends_with_filter(_: BaseAffair) -> bool:
        return isinstance(_, ChatAffair) and _.event.raw_message.endswith(suffix)
    return pypbbot.plugin.onFilter(_on_ends_with_filter, priority)

from pypbbot.typing import LoadingEvent
def onLoading(priority: HandlerPriority = HandlerPriority.NORMAL):
    def _on_loading(_: BaseAffair) -> bool:
        return isinstance(_.event, LoadingEvent)
    return pypbbot.plugin.onFilter(_on_loading, priority)

from pypbbot.typing import UnloadingEvent
def onUnloading(priority: HandlerPriority = HandlerPriority.NORMAL):
    def _on_unloading(_: BaseAffair) -> bool:
        return isinstance(_.event, UnloadingEvent)
    return pypbbot.plugin.onFilter(_on_unloading, priority)
