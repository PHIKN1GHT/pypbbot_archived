from enum import Enum
from typing import Optional
from pypbbot.types import ProtobufBotEvent
import pypbbot

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
    event: Optional[ProtobufBotEvent]

def all(_: BaseAffair) -> bool:
    return True

def onAll(priority: HandlerPriority = HandlerPriority.NORMAL):
    return pypbbot.plugin.onFilter(all, priority)


