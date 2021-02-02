from functools import partial
import os

from pypbbot.protocol import *
from pypbbot.types import ProtobufBotEvent, ProtobufBotAPI
from pypbbot import server
from pypbbot.utils import Clips
from typing import Type, Dict, Callable, Awaitable, Optional, Union

class BaseDriver:
    def __init__(self, botId: int):
        self.botId = botId
        self._handler_registry: Dict[Type[ProtobufBotEvent], Callable[[ProtobufBotEvent], Awaitable[Optional[bool]]]] = {}
        self._handler_registry[PrivateMessageEvent] = getattr(self, 'onPrivateMessage')
        self._handler_registry[GroupMessageEvent] = getattr(self, 'onGroupMessage')
        self._handler_registry[GroupUploadNoticeEvent] = getattr(self, 'onGroupUploadNotice')
        self._handler_registry[GroupAdminNoticeEvent] = getattr(self, 'onGroupAdminNotice')
        self._handler_registry[GroupDecreaseNoticeEvent] = getattr(self, 'onGroupDecreaseNotice')
        self._handler_registry[GroupIncreaseNoticeEvent] = getattr(self, 'onGroupIncreaseNotice')
        self._handler_registry[GroupBanNoticeEvent] = getattr(self, 'onGroupBanNotice')
        self._handler_registry[FriendAddNoticeEvent] = getattr(self, 'onFriendAddNotice')
        self._handler_registry[GroupRecallNoticeEvent] = getattr(self, 'onGroupRecallNotice')
        self._handler_registry[FriendRecallNoticeEvent] = getattr(self, 'onFriendRecallNotice')
        self._handler_registry[FriendRequestEvent] = getattr(self, 'onFriendRequest')
        self._handler_registry[GroupRequestEvent] = getattr(self, 'onGroupRequest')

    async def handle(self, event: ProtobufBotEvent):
        if type(event) in self._handler_registry.keys():
            await self._handler_registry[type(event)](event)
    

    async def sendBackClips(self, event: Union[PrivateMessageEvent, GroupMessageEvent], clips: Union[Clips, str, int, float]) -> ProtobufBotAPI:
        if isinstance(event, PrivateMessageEvent):
            return await self.sendPrivateClips(event.user_id, clips)
        elif isinstance(event, GroupMessageEvent):
            return await self.sendGroupClips(event.group_id, clips)

    async def onPrivateMessage(self, event: PrivateMessageEvent) -> Optional[bool]:
        pass
    async def onGroupMessage(self, event: GroupMessageEvent) -> Optional[bool]:
        pass
    async def onGroupUploadNotice(self, event: GroupUploadNoticeEvent) -> Optional[bool]:
        pass
    async def onGroupAdminNotice(self, event: GroupAdminNoticeEvent) -> Optional[bool]:
        pass
    async def onGroupDecreaseNotice(self, event: GroupDecreaseNoticeEvent) -> Optional[bool]:
        pass
    async def onGroupIncreaseNotice(self, event: GroupIncreaseNoticeEvent) -> Optional[bool]:
        pass
    async def onGroupBanNotice(self, event: GroupBanNoticeEvent) -> Optional[bool]:
        pass
    async def onFriendAddNotice(self, event: FriendAddNoticeEvent) -> Optional[bool]:
        pass
    async def onGroupRecallNotice(self, event: GroupRecallNoticeEvent) -> Optional[bool]:
        pass
    async def onFriendRecallNotice(self, event: FriendRecallNoticeEvent) -> Optional[bool]:
        pass
    async def onFriendRequest(self, event: FriendRequestEvent) -> Optional[bool]:
        pass
    async def onGroupRequest(self, event: GroupRequestEvent) -> Optional[bool]:
        pass

    async def sendPrivateClips(self, user_id: int, clips: Union[Clips, str, int, float]) -> ProtobufBotAPI:
        clips = Clips() + clips
        api_content = SendPrivateMsgReq()
        api_content.user_id, auto_escape = user_id, True
        for datum in clips._data:
            textmsg = Message()
            textmsg.type = datum[0]
            for item in datum[1].keys():
                textmsg.data[item] = datum[1][item]
            api_content.message.append(textmsg)
        return await server.send_frame(self, api_content)

    async def sendGroupClips(self, group_id: int, clips: Union[Clips, str, int, float]) -> ProtobufBotAPI:
        clips = Clips() + clips
        api_content = SendGroupMsgReq()
        api_content.group_id, auto_escape = group_id, True
        for datum in clips._data:
            textmsg = Message()
            textmsg.type = datum[0]
            for item in datum[1].keys():
                textmsg.data[item] = datum[1][item]
            api_content.message.append(textmsg)
        return await server.send_frame(self, api_content)

    async def recallMessage(self, message_id: int) -> ProtobufBotAPI:
        api_content = DeleteMsgReq()
        api_content.message_id = message_id
        return await server.send_frame(self, api_content)

from pypbbot.utils import SingletonType
from pypbbot.plugin import _handle as handleAffair
from pypbbot.affairs import BaseAffair
import pkgutil
class PluginDriver(BaseDriver, metaclass=SingletonType):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, plugin_path='plugins'):
        pass

    async def handle(self, event: ProtobufBotEvent):
        affair = BaseAffair()
        affair.event = event
        handleAffair(affair)
        #if type(event) in self._handler_registry.keys():
        #    await self._handler_registry[type(event)](event)
