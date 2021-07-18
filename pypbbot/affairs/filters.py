from __future__ import annotations
from typing import List

import typing
if typing.TYPE_CHECKING:
    from typing import Callable
    from pypbbot.typing import Event
    from pypbbot.driver import BaseDriver, AffairDriver
    from pypbbot.affairs import HandlerPriority, BaseAffair, Handler, Filter

from pypbbot.logging import logger
from pypbbot.utils import sendBackClipsTo, Clips, partial_filter
from pypbbot.affairs import ChatAffair
from pypbbot.typing import LoadingEvent, UnloadingEvent

__all__ = ['_unfilterable', '_on_loading', '_on_unloading',
           '_on_starts_with_filter', '_union_filter', 'UnionFilter']


def _unfilterable(_: BaseAffair) -> bool:
    return True


def _on_loading(_: BaseAffair) -> bool:
    return isinstance(_.event, LoadingEvent)


def _on_unloading(_: BaseAffair) -> bool:
    return isinstance(_.event, UnloadingEvent)


def _on_starts_with_filter(prefix: str, _: BaseAffair) -> bool:
    return (isinstance(_, ChatAffair)) and (_.event.raw_message.startswith(prefix))


def _union_filter(handlers: List[Handler], affair: BaseAffair) -> bool:
    for handler in handlers:
        if handler(affair):
            return True
    return False


def UnionFilter(handlers: List[Handler]) -> Filter:
    return partial_filter(_union_filter, (handlers, ))
