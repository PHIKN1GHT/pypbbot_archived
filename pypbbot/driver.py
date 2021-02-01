from pypbbot.protocol import *
from pypbbot.types import ProtobufBotEvent, ProtobufBotAPI
from pypbbot import server
from typing import Type, Dict, Callable, Awaitable, Optional

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

    async def sendPrivateTextMessage(self, user_id: int, text: str) -> ProtobufBotAPI:
        textmsg = Message()
        textmsg.type, textmsg.data["text"] = "text", text
        api_content = SendPrivateMsgReq()
        api_content.message.append(textmsg)
        api_content.user_id, auto_escape = user_id, True
        return await server.send_frame(self, api_content)

    async def sendGroupTextMessage(self, group_id: int, text: str) -> ProtobufBotAPI:
        textmsg = Message()
        textmsg.type, textmsg.data["text"] = "text", text
        api_content = SendGroupMsgReq()
        api_content.message.append(textmsg)
        api_content.group_id, auto_escape = group_id, True
        return await server.send_frame(self, api_content)
