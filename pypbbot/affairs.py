from enum import Enum
from typing import Optional
from pypbbot.types import ProtobufBotEvent

import pypbbot
from pypbbot.driver import BaseDriver

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
    #name: str = __name__
    event: Optional[ProtobufBotEvent]
    driver: Optional[BaseDriver]
    finished: bool

class ChatAffair(BaseAffair):
    pass
    #def send(self, clips: Clips):
    #    pass


def unfilterable(priority: HandlerPriority = HandlerPriority.NORMAL):
    def _unfilterable(_: BaseAffair) -> bool:
        return True
    return pypbbot.plugin.onFilter(_unfilterable, priority)

def combined():
    pass

def onLoading():
    pass

def onUnloading():
    pass

def onPrivate():
    pass

def onGroup():
    pass


