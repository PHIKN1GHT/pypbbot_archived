from pypbbot.protocol import *
from pypbbot import server

class BaseDriver:
    def __init__(self, botId):
        self.botId = botId
        self._handler_registry = {}
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

    async def handle(self, event):
        if type(event) in self._handler_registry.keys():
            await self._handler_registry[type(event)](event)

    async def onPrivateMessage(self, event):
        pass
    async def onGroupMessage(self, event):
        pass
    async def onGroupUploadNotice(self, event):
        pass
    async def onGroupAdminNotice(self, event):
        pass
    async def onGroupDecreaseNotice(self, event):
        pass
    async def onGroupIncreaseNotice(self, event):
        pass
    async def onGroupBanNotice(self, event):
        pass
    async def onFriendAddNotice(self, event):
        pass
    async def onGroupRecallNotice(self, event):
        pass
    async def onFriendRecallNotice(self, event):
        pass
    async def onFriendRequest(self, event):
        pass
    async def onGroupRequest(self, event):
        pass

    async def sendPrivateTextMessage(self, user_id, text):
        textmsg = Message()
        textmsg.type, textmsg.data["text"] = "text", text
        api_content = SendPrivateMsgReq()
        api_content.message.append(textmsg)
        api_content.user_id, auto_escape = user_id, True
        await server.send_frame(self, api_content)

    async def sendGroupTextMessage(self, group_id, text):
        textmsg = Message()
        textmsg.type, textmsg.data["text"] = "text", text
        api_content = SendGroupMsgReq()
        api_content.message.append(textmsg)
        api_content.group_id, auto_escape = group_id, True
        await server.send_frame(self, api_content)
