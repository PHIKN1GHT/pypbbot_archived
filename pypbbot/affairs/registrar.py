
from __future__ import annotations
from .filters import _on_unloading
from .filters import _on_loading
from pypbbot.protocol import GroupMessageEvent, GroupRecallNoticeEvent
from pypbbot.protocol import PrivateMessageEvent, FriendRecallNoticeEvent
from .filters import _unfilterable
from pypbbot.typing import UnloadingEvent
from pypbbot.typing import LoadingEvent
from .filters import _on_starts_with_filter

import typing
if typing.TYPE_CHECKING:
    from typing import Optional, Union, Callable, Coroutine, Any
    from pypbbot.driver import BaseDriver, AffairDriver
    from pypbbot.typing import Event
    from pypbbot.affairs import BaseAffair, ChatAffair, Handler, Filter, DecoratedHandler

import functools
from pypbbot.logging import logger
from pypbbot.plugin import _register
from pypbbot.utils import partial_filter
from pypbbot.affairs import HandlerPriority, ChatAffair

__all__ = ['useFilter', 'unfilterable', 'onPrivateMessage', 'onGroupMessage',
           'onStartsWith', 'onEndsWith', 'onLoading', 'onUnloading', 'onMessage']


def useFilter(ftr: Filter, priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    '''An decorator to register an affair handler for a specific affait filter.
    Args:
        ftr: the filter function.
        priority: the priority of the handler
    '''
    try:
        name = getattr(ftr, '__name__')
    except AttributeError:
        logger.error(
            'Unnamed filter funcion detected. You SHOULD NOT use lambda expression.')
        setattr(ftr, '__name__', '[unknown]')

    try:
        getattr(useFilter, ftr.__name__)
    except AttributeError:
        setattr(useFilter, ftr.__name__, ftr)

    def decorator(func: Handler):  # type: ignore
        # DO NOT USE LAMBDA EXPRESSION
        _register(ftr.__name__, ftr, func, priority)

        @functools.wraps(func)
        def wrapper(affair: BaseAffair) -> Coroutine[Any, Any, None]:
            return func(affair)
        return wrapper
    return decorator


def unfilterable(priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    return useFilter(_unfilterable, priority)


def onPrivateMessage(priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    def _private_message_filter(_: BaseAffair) -> bool:
        return isinstance(_.event, PrivateMessageEvent)
    return useFilter(_private_message_filter, priority)


def onGroupMessage(priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    def _group_message_filter(_: BaseAffair) -> bool:
        return isinstance(_.event, GroupMessageEvent)
    return useFilter(_group_message_filter, priority)


def onStartsWith(prefix: str, priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    _filter = partial_filter(_on_starts_with_filter, (prefix, ))
    return useFilter(_filter, priority)


def onEndsWith(suffix: str, priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    def _on_ends_with_filter(_: BaseAffair) -> bool:
        return isinstance(_, ChatAffair) and _.event.raw_message.endswith(suffix)
    return useFilter(_on_ends_with_filter, priority)


def onLoading(priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    return useFilter(_on_loading, priority)


def onGroupRecall(group_id=None, priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    def _filter(_: BaseAffair) -> bool:
        return isinstance(_.event, GroupRecallNoticeEvent) if group_id is None else (isinstance(_.event, GroupRecallNoticeEvent) and _.event.group_id == group_id)
    return useFilter(_filter, priority)


def onFriendRecall(user_id=None, priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    def _filter(_: BaseAffair) -> bool:
        return isinstance(_.event, FriendRecallNoticeEvent) if friend_id is None else (isinstance(_.event, GroupRecallNoticeEvent) and _.event.user_id == user_id)
    return useFilter(_filter, priority)


def onUnloading(priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    return useFilter(_on_unloading, priority)


def onMessage(priority: HandlerPriority = HandlerPriority.NORMAL) -> DecoratedHandler:
    def _message_filter(_: BaseAffair) -> bool:
        return isinstance(_, ChatAffair)
    return useFilter(_message_filter, priority)


'''
def starts_with(sth) -> :
    def inner_func(sth):
        print(sth)
    try:
        starts_with.inner
    except AttributeError:
        starts_with.inner = inner_func
        
    print(repr(starts_with.inner))
    starts_with.inner(sth)
'''
