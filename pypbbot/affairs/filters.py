from __future__ import annotations
from typing import List, Any, Tuple, Dict
from returns.curry import partial

import typing
if typing.TYPE_CHECKING:
    from pypbbot.affairs import BaseAffair, Handler, Filter

from pypbbot.affairs import ChatAffair
from pypbbot.typing import LoadingEvent, UnloadingEvent

__all__ = ['_unfilterable', '_on_loading', '_on_unloading',
           '_on_starts_with_filter', '_union_filter', 'UnionFilter']


def partial_filter(func: Any, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Filter:
    pfunc = partial(func, *args, **kwargs)
    setattr(pfunc, '__name__', "{}[{}]".format(
        partial.__name__, func.__name__))
    return pfunc


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
