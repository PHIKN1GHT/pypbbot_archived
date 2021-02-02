from typing import Callable, Type, Dict, Tuple
from queue import PriorityQueue
from pypbbot.log import logger
from pypbbot.affairs import BaseAffair, HandlerPriority

class CallableHandler():
    def __init__(self, func: Callable[[BaseAffair], bool], priority):
        self._func = func
        self._priority = priority
        
    def __eq__(self, other):
        return self._priority == other._priority

    def __lt__(self, other):
        return self._priority < other._priority

_handlers: Dict[str, Tuple[Callable[[BaseAffair], bool], PriorityQueue]] = {}

def _register(affair_filter: Callable[[BaseAffair], bool], func: Callable[[BaseAffair], bool], priority: HandlerPriority):
    logger.debug('Registering handler [{}] for filter [{}] ...'.format(func.__name__, affair_filter.__name__))
    if not affair_filter.__name__ in _handlers.keys():
        _handlers[affair_filter.__name__] = (affair_filter, PriorityQueue())
    _, pqueue = _handlers[affair_filter.__name__]
    pqueue.put(CallableHandler(func, priority))

def _handle(affair: BaseAffair):
    for _, (affair_filter, pqueue) in _handlers.items():
        print(pqueue.queue)
        for handler in pqueue.queue:
            handler._func(affair)

import functools
def onFilter(filter_func: Callable[[BaseAffair], bool], priority: HandlerPriority = HandlerPriority.NORMAL):
    def decorator(func: Callable[[BaseAffair], bool]):
        _register(filter_func, func, priority) # DO NOT USE LAMBDA EXPRESSION OR INNER FUNCTION
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        return wrapper
    return decorator

import pkgutil, os
from pkgutil import ImpLoader
from importlib.abc import PathEntryFinder, MetaPathFinder
from types import ModuleType

_loadedPlugins: Dict[str, ModuleType] = {}
def load_plugins(*plugin_dir: str):
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
