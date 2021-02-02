from typing import List, Tuple, Dict, TypeVar, Union, Type
from pypbbot.types import ProtobufBotMessage
import copy

def in_lower_case(text: str) -> str:
    lst: List[str] = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)

    return "".join(lst).lower()

T = TypeVar('T', bound='Clips') 
class Clips():
    def __init__(self):
        self._data: List[Tuple[str, Dict[str,str]]] = []
    
    def append(self: T, data: Tuple[str, Dict[str,str]]) -> T:
        self._data.append(data)
        return self

    def __add__(self: T, other: Union[T, str, int, float]) -> T:
        clips = copy.deepcopy(self)
        if isinstance(other, Clips):
            clips._data += copy.deepcopy(other._data)
        elif isinstance(other, str) or isinstance(other, int) or isinstance(other, float):
            clips._data += Clips.from_str(str(other))._data
        return clips
    
    def __radd__(self: T, other: Union[T, str, int, float]) -> T:
        clips = copy.deepcopy(self)
        if isinstance(other, Clips):
            clips._data = copy.deepcopy(other._data) + clips._data
        else:
            clips._data = Clips.from_str(str(other))._data + clips._data
        return clips

    def __str__(self: T) -> str:
        reprstr = ''
        for datum in self._data:
            reprstr += datum[1]['text'] if datum[0] == 'text' else str(datum[1])
        return reprstr

    @classmethod
    def from_str(cls: Type[T], text: str) -> T:
        return cls().append(("text", {"text": text}))

    @classmethod
    def from_image_url(cls: Type[T], url: str) -> T:
        return cls().append(("image", {"url": url}))

import threading
class SingletonType(type):
    _instance_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
        return cls._instance
