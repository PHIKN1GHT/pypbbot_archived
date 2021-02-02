
from typing import Callable, Type, Dict
from queue import PriorityQueue
from enum import Enum

class AffairPriority(Enum):
    SYSTEM = 0 # SHOULD NOT USED BY PLUGINS
    VERY_HIGH = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    VERY_LOW = 5

    def __lt__(self, other):
        return self.value < other.value

class BaseAffair:
    pass

class CallableHandler():
    def __init__(self, func: Callable[[BaseAffair], bool], priority):
        self._func = func
        self._priority = priority
        
    def __eq__(self, other):
        return self._priority == other._priority

    def __lt__(self, other):
        return self._priority < other._priority

_handlers: Dict[Callable[[BaseAffair], bool], PriorityQueue] = {}

def _register(affair_filter: Callable[[BaseAffair], bool], func: Callable[[BaseAffair], bool], priority: AffairPriority):
    if not affair_filter in _handlers.keys():
        _handlers[affair_filter] = PriorityQueue()
    _handlers[affair_filter].put(CallableHandler(func, priority))

def _handle(affair: BaseAffair):
    print('handling', _handlers.keys())
    for affair_filter, pqueue in _handlers.items():
        print(affair_filter(affair))
        if affair_filter(affair):
            while pqueue.qsize() > 0:
                task = pqueue.get()
                print(task._func, task._priority)
                task._func(affair)

import functools
def onFilter(filter_func: Callable[[BaseAffair], bool], priority: AffairPriority = AffairPriority.NORMAL):
    def decorator(func: Callable[[BaseAffair], bool]):
        _register(filter_func, func, priority) # DO NOT USE LAMBDA EXPRESSION OR INNER FUNCTION
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        return wrapper
    return decorator

def all(_: BaseAffair) -> bool:
    return True

def onAll(priority: AffairPriority = AffairPriority.NORMAL):
    return onFilter(all, priority)

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
        print('loading ', name)
        if isinstance(module_finder, PathEntryFinder): # Hack for Type Check
            module = module_finder.find_module(name)
        elif isinstance(module_finder, MetaPathFinder):
            module = module_finder.find_module(name, None) # SourceFileLoader
        if module is not None:
            _loadedPlugins[name] = module.load_module(name)
    return _loadedPlugins
