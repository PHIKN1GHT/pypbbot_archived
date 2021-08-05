from __future__ import annotations
import os
import pkgutil
from types import ModuleType
from importlib.abc import PathEntryFinder, MetaPathFinder

import typing
if typing.TYPE_CHECKING:
    from pypbbot.affairs import BaseAffair, HandlerPriority, Handler, Filter
    from typing import Dict, Tuple, List
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


_handlers: Dict[str, List[Tuple[Filter,
                                PriorityQueue[CallableHandler]]]] = {}


def _register(name: str, affair_filter: Filter, func: Handler, priority: HandlerPriority) -> None:
    logger.debug('Registering handler [{}] for filter [{}] ...'.format(
        func.__name__, affair_filter.__name__))
    pqueue: PriorityQueue[CallableHandler] = PriorityQueue()
    _affair_filter: Filter = affair_filter
    if not name in _handlers.keys():
        _handlers[name] = [(_affair_filter, pqueue)]
    else:
        _handlers[name].append((_affair_filter, pqueue))
    pqueue.put(CallableHandler(func, priority))


async def _handle(affair: BaseAffair) -> None:
    logger.warning('Handling [{}]'.format(affair))
    for _, filterList in _handlers.items():
        for affair_filter, pqueue in filterList:
            if affair_filter(affair):
                logger.debug('Pass to [{}]'.format(_))
                for handler in pqueue.queue:
                    await handler._func(affair)


_loadedPlugins: Dict[str, ModuleType] = {}


async def load_plugins(*plugin_dir: str) -> Dict[str, ModuleType]:
    for _dir in plugin_dir:
        if not os.path.exists(_dir):
            os.makedirs(_dir)

    for module_finder, name, _ in pkgutil.iter_modules(plugin_dir):
        logger.info('Loading module [{}] ...'.format(name))
        if isinstance(module_finder, PathEntryFinder):  # Hack for Type Check
            module = module_finder.find_module(name)
        elif isinstance(module_finder, MetaPathFinder):
            module = module_finder.find_module(name, None)  # SourceFileLoader
        if module is not None:
            _loadedPlugins[name] = module.load_module(name)
    return _loadedPlugins
