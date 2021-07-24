from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    pass

from typing import Callable, Coroutine, Any, TypeVar
from .builtin import HandlerPriority, BaseAffair, ChatAffair
from .registrar import onEndsWith, onGroupMessage, onMessage, onStartsWith, onLoading, onUnloading, onFriendRecall, onGroupRecall

__all__ = ['HandlerPriority', 'BaseAffair', 'ChatAffair', 'onEndsWith',
           'onGroupMessage', 'onMessage', 'onStartsWith', 'onLoading', 'onUnloading', 'onFriendRecall', 'onGroupRecall']

Filter = Callable[[BaseAffair], bool]
Handler = Callable[[BaseAffair], Coroutine[Any, Any, None]]
UnverifiedHandler = Callable[[Any], Coroutine[Any, Any, Any]]
HandlerDecorator = Callable[[UnverifiedHandler], UnverifiedHandler]
