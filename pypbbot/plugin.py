from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    from pypbbot.affairs import BaseAffair, HandlerPriority, Handler, Filter
    from typing import Callable, Type, Dict, Tuple

from queue import PriorityQueue
from pypbbot.logging import logger
import typing


class CallableHandler():
    def __init__(self, func: Handler, priority: HandlerPriority) -> None:
        self._func = func
        self._priority = priority
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CallableHandler):
            return NotImplemented
        return self._priority == other._priority

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, CallableHandler):
            return NotImplemented
        return self._priority < other._priority

_handlers: Dict[str, Tuple[Filter, PriorityQueue[CallableHandler]]] = {}

def _register(name: str, affair_filter: Filter, func: Handler, priority: HandlerPriority) -> None:
    logger.debug('Registering handler [{}] for filter [{}] ...'.format(func.__name__, affair_filter.__name__))
    if not name in _handlers.keys():
        _handlers[name] = (affair_filter, PriorityQueue())
    _, pqueue = _handlers[name]
    pqueue.put(CallableHandler(func, priority))

async def _handle(affair: BaseAffair) -> None:
    logger.warning('Handling [{}]'.format(affair))
    for _, (affair_filter, pqueue) in _handlers.items():
        if affair_filter(affair):
            logger.debug('Pass to [{}]'.format(_))
            for handler in pqueue.queue:
                await handler._func(affair)


import pkgutil, os
from pkgutil import ImpLoader
from importlib.abc import PathEntryFinder, MetaPathFinder
from types import ModuleType

_loadedPlugins: Dict[str, ModuleType] = {}
async def load_plugins(*plugin_dir: str) -> Dict[str, ModuleType]:
    for _dir in plugin_dir:
        if not os.path.exists(_dir):
            os.makedirs(_dir)
    for module_finder, name, _ in pkgutil.iter_modules(plugin_dir):
        logger.info('Loading module [{}] ...'.format(name))
        if isinstance(module_finder, PathEntryFinder): # Hack for Type Check
            module = module_finder.find_module(name)
        elif isinstance(module_finder, MetaPathFinder):
            module = module_finder.find_module(name, None) # SourceFileLoader
        if module is not None:
            _loadedPlugins[name] = module.load_module(name)
    return _loadedPlugins
