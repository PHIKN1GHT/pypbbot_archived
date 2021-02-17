
from enum import Enum
from typing import Optional, Union
import pypbbot
from pypbbot.typing import Event
from pypbbot.logging import logger
from pypbbot.driver import BaseDriver, AffairDriver
from pypbbot.utils import sendBackClipsTo, Clips
from pypbbot.affairs import HandlerPriority, BaseAffair, ChatAffair

from .filters import _unfilterable
def unfilterable(priority: HandlerPriority = HandlerPriority.NORMAL):
    return pypbbot.plugin.onFilter(_unfilterable, priority)


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

from .filters import _on_loading
from pypbbot.typing import LoadingEvent
def onLoading(priority: HandlerPriority = HandlerPriority.NORMAL):
    return pypbbot.plugin.onFilter(_on_loading, priority)

from .filters import _on_unloading
from pypbbot.typing import UnloadingEvent
def onUnloading(priority: HandlerPriority = HandlerPriority.NORMAL):
    return pypbbot.plugin.onFilter(_on_unloading, priority)

def onMessage(priority: HandlerPriority = HandlerPriority.NORMAL):
    def _message_filter(_: BaseAffair) -> bool:
        return isinstance(_, ChatAffair)
    return pypbbot.plugin.onFilter(_message_filter, priority)