from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    pass

from typing import Callable, Coroutine, Any
from .builtin import HandlerPriority, BaseAffair, ChatAffair
from .registrar import onEndsWith, onGroupMessage, onMessage, onStartsWith, onLoading, onUnloading

__all__ = ['HandlerPriority','BaseAffair','ChatAffair','onEndsWith','onGroupMessage','onMessage','onStartsWith','onLoading','onUnloading']

Filter = Callable[[BaseAffair], bool]
Handler = Callable[[BaseAffair], Coroutine[Any, Any, None]]
DecoratedHandler = Callable[[Handler], Coroutine[Any, Any, None]]
