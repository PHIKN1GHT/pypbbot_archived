from enum import Enum
from typing import Optional, Union, Any, Dict
from pypbbot.typing import Event
from pypbbot.logging import logger
from pypbbot.driver import BaseDriver, AffairDriver
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
    def __init__(self, driver: AffairDriver, event: Event):
        logger.debug('A new affair has been created for event [{}]'.format(type(event)))
        self.event: Optional[Event] = event
        self.states: Dict[str, Any] = {}
        self.driver = driver
        self.finished = False

from pypbbot.typing import GroupMessageEvent, PrivateMessageEvent
class ChatAffair(BaseAffair):
    def __init__(self, driver, event: Union[GroupMessageEvent, PrivateMessageEvent], sender_id):
        self.event: Union[GroupMessageEvent, PrivateMessageEvent] = event
        self.driver = driver
        self.receiver_id = event.self_id
        self.sender_id = sender_id
        self.raw_message = event.raw_message

    async def send(self, clips: Union[Clips, str, int, float]):
        await sendBackClipsTo(self.event, clips)
