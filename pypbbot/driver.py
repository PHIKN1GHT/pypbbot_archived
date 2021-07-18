from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    from typing import Type, Dict, Optional, Tuple, Any
    from pypbbot.typing import ProtobufBotAPI

import os
from typing import Callable, Awaitable, Union
from pypbbot.protocol import *
from pypbbot import server
from pypbbot.utils import Clips, sendBackClipsTo, SingletonType
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent
from pypbbot.logging import logger
from pypbbot.plugin import _handle as handleAffair
from pypbbot.typing import Event


class BaseDriver:
    def __init__(self, botId: int):
        self.botId = botId
        self._handler_registry: Dict[Type[Event], Callable[[
            Event], Awaitable[Optional[bool]]]] = {}
        self._handler_registry[PrivateMessageEvent] = getattr(
            self, 'onPrivateMessage')
        self._handler_registry[GroupMessageEvent] = getattr(
            self, 'onGroupMessage')
        self._handler_registry[GroupUploadNoticeEvent] = getattr(
            self, 'onGroupUploadNotice')
        self._handler_registry[GroupAdminNoticeEvent] = getattr(
            self, 'onGroupAdminNotice')
        self._handler_registry[GroupDecreaseNoticeEvent] = getattr(
            self, 'onGroupDecreaseNotice')
        self._handler_registry[GroupIncreaseNoticeEvent] = getattr(
            self, 'onGroupIncreaseNotice')
        self._handler_registry[GroupBanNoticeEvent] = getattr(
            self, 'onGroupBanNotice')
        self._handler_registry[FriendAddNoticeEvent] = getattr(
            self, 'onFriendAddNotice')
        self._handler_registry[GroupRecallNoticeEvent] = getattr(
            self, 'onGroupRecallNotice')
        self._handler_registry[FriendRecallNoticeEvent] = getattr(
            self, 'onFriendRecallNotice')
        self._handler_registry[FriendRequestEvent] = getattr(
            self, 'onFriendRequest')
        self._handler_registry[GroupRequestEvent] = getattr(
            self, 'onGroupRequest')

    async def handle(self, event: Event) -> None:
        if type(event) in self._handler_registry.keys():
            await self._handler_registry[type(event)](event)

    async def sendBackClips(self, event: Union[PrivateMessageEvent, GroupMessageEvent],
                            clips: Union[Clips, str, int, float]) -> Optional[ProtobufBotAPI]:
        return await sendBackClipsTo(event, clips)

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

    async def sendPrivateClips(self, user_id: int, clips: Union[Clips, str, int, float]) -> Optional[ProtobufBotAPI]:
        clips = Clips() + clips
        api_content = SendPrivateMsgReq()
        api_content.user_id, auto_escape = user_id, True
        api_content.message.extend(clips.toMessageList())
        return await server.send_frame(self.botId, api_content)

    async def sendGroupClips(self, group_id: int, clips: Union[Clips, str, int, float]) -> Optional[ProtobufBotAPI]:
        clips = Clips() + clips
        api_content = SendGroupMsgReq()
        api_content.group_id, auto_escape = group_id, True
        api_content.message.extend(clips.toMessageList())
        return await server.send_frame(self.botId, api_content)

    async def recallMessage(self, message_id: int) -> Optional[ProtobufBotAPI]:
        api_content = DeleteMsgReq()
        api_content.message_id = message_id
        return await server.send_frame(self.botId, api_content)


class AffairDriver(BaseDriver, metaclass=SingletonType):
    def __init__(self) -> None:
        pass

    def __new__(cls, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
        return object.__new__(cls)

    async def handle(self, event: Event) -> None:
        from pypbbot.affairs import BaseAffair, ChatAffair
        affair: BaseAffair
        if isinstance(event, PrivateMessageEvent):
            affair = ChatAffair(self, event, event.user_id)
        elif isinstance(event, GroupMessageEvent):
            affair = ChatAffair(self, event, event.Sender.user_id)
        else:
            affair = BaseAffair(self, event)
        await handleAffair(affair)


FunctionalDriver = Callable[[Event], Awaitable[None]]
Drivable = Union[BaseDriver, FunctionalDriver]
