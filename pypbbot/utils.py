from typing import List, Tuple, Dict, TypeVar, Union, Type
from pypbbot.typing import ProtobufBotMessage as Message
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

    def toMessageList(self: T) -> List[Message]:
        lst: List[Message] = []
        for datum in self._data:
            textmsg = Message()
            textmsg.type = datum[0]
            for item in datum[1].keys():
                textmsg.data[item] = datum[1][item]
            lst.append(textmsg)
        return lst

    @classmethod
    def from_str(cls: Type[T], text: str) -> T:
        return cls().append(("text", {"text": text}))

    @classmethod
    def from_image_url(cls: Type[T], url: str) -> T:
        return cls().append(("image", {"url": url}))


from collections import OrderedDict
from typing import Optional
from asyncio import Future
# str, Future

class LRUResponseCache:
    def __init__(self, capacity: int = 65536):
        self.cache: OrderedDict[str, Future] = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> Future:
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, value: Future) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)

    def hasKey(self, key: str) -> bool:
        return key in self.cache.keys()

    def remove(self, key: str) -> None:
        self.cache.pop(key)