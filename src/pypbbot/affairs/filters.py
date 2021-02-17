
from enum import Enum
from typing import Optional, Union
import pypbbot
from pypbbot.typing import Event
from pypbbot.logging import logger
from pypbbot.driver import BaseDriver, AffairDriver
from pypbbot.utils import sendBackClipsTo, Clips
from pypbbot.affairs import HandlerPriority, BaseAffair, ChatAffair
from pypbbot.typing import LoadingEvent, UnloadingEvent

def _unfilterable(_: BaseAffair) -> bool:
        return True

def _on_loading(_: BaseAffair) -> bool:
    return isinstance(_.event, LoadingEvent)

def _on_unloading(_: BaseAffair) -> bool:
    return isinstance(_.event, UnloadingEvent)
'''

'''