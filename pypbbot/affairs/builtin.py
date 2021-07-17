from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    from typing import Optional, Union, Any, Dict
    from pypbbot.driver import AffairDriver
    from pypbbot.typing import Event
    from pypbbot.utils import Clips
    from pypbbot.protocol import GroupMessageEvent, PrivateMessageEvent

from enum import Enum
from pypbbot.logging import logger
from pypbbot.utils import sendBackClipsTo

__all__ = ['HandlerPriority', 'BaseAffair', 'ChatAffair']

class HandlerPriority(Enum):
    SYSTEM = 0 # SHOULD NOT USED BY PLUGINS
    VERY_HIGH = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    VERY_LOW = 5

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, HandlerPriority):
            return NotImplemented
        return self.value < other.value

class BaseAffair:
    def __init__(self, driver: AffairDriver, event: Event) -> None:
        logger.debug('A new affair has been created for event [{}]'.format(type(event)))
        self.event: Optional[Event] = event
        self.driver: AffairDriver = driver
        self.states: Dict[str, Any] = {}
        self.finished: bool = False
        return

class ChatAffair(BaseAffair):
    def __init__(self, driver: AffairDriver, event: Union[GroupMessageEvent, PrivateMessageEvent], sender_id: int) -> None:
        self.event: Union[GroupMessageEvent, PrivateMessageEvent] = event
        self.driver: AffairDriver = driver
        self.receiver_id: int = event.self_id
        self.sender_id: int = sender_id
        self.raw_message: str = event.raw_message
        return

    async def send(self, clips: Union[Clips, str, int, float]) -> Any:
        return await sendBackClipsTo(self.event, clips)
