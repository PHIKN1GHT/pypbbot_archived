
from typing import Callable, Type, Dict
from queue import PriorityQueue
from enum import Enum

class AffairPriority(Enum):
    SYSTEM = 0 # Should not used by plugins
    VERY_HIGH = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    VERY_LOW = 5

    def __lt__(self, other):
        return self.value < other.value

class BaseAffair:
    msg = ''
    pass

class CallableHandler():
    def __init__(self, func: Callable[[BaseAffair], bool], priority):
        self._func = func
        self._priority = priority
        
    def __eq__(self, other):
        return self._priority == other._priority

    def __lt__(self, other):
        return self._priority < other._priority

_handlers: Dict[Type[BaseAffair], PriorityQueue] = {}

def _register(affair_type: Type[BaseAffair], func: Callable[[BaseAffair], bool], priority: AffairPriority):
    if not affair_type in _handlers.keys():
        _handlers[affair_type] = PriorityQueue()
    _handlers[affair_type].put(CallableHandler(func, priority))
        
def _handle(affair: BaseAffair):
    if type(affair) in _handlers.keys():
        pqueue = _handlers[type(affair)]
        while pqueue.qsize() > 0:
            task = pqueue.get()
            print(task._func, task._priority)
            task._func(affair)

import functools
def onLoad(priority: AffairPriority = AffairPriority.NORMAL):
    def decorator(func: Callable[[BaseAffair], bool]):
        _register(BaseAffair, func, priority)
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
        if isinstance(module_finder, PathEntryFinder): # Hack for Type Check
            module = module_finder.find_module(name)
        elif isinstance(module_finder, MetaPathFinder):
            module = module_finder.find_module(name, None)
        if isinstance(module, ImpLoader):
            _loadedPlugins[name] = module.load_module(name)
    return _loadedPlugins
