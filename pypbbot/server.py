import sys, os
import uvicorn

from fastapi import FastAPI, WebSocket

from pypbbot.protocol.onebot_frame_pb2 import Frame
from pypbbot.protocol.onebot_event_pb2 import PrivateMessageEvent, GroupMessageEvent
from pypbbot.protocol.onebot_api_pb2 import SendPrivateMsgReq, SendGroupMsgReq
from pypbbot.protocol.onebot_base_pb2 import Message

app = FastAPI()

@app.websocket("/ws/test/")
async def recv_msg(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        msg = Frame()
        msg.ParseFromString(data) 
        print(msg.IsInitialized())

        
        if type(getattr(msg, msg.WhichOneof('data'))) == PrivateMessageEvent:
            print('RECV: ', msg)
            pmsg = getattr(msg, msg.WhichOneof('data'))

            frame = Frame()
            frame.botId = pmsg.self_id
            frame.frame_type = Frame.FrameType.TSendPrivateMsgReq
            frame.echo = ""
            frame.ok = True

            retmsg = SendPrivateMsgReq()
            msgtext = Message()
            msgtext.type = "text"
            msgtext.data["text"] = 'qwq!'
            retmsg.message.append(msgtext)
            retmsg.user_id = pmsg.user_id
            retmsg.auto_escape = True
            frame.send_private_msg_req.CopyFrom(retmsg)

            data = frame.SerializeToString()
            await websocket.send_bytes(data)
        elif type(getattr(msg, msg.WhichOneof('data'))) == GroupMessageEvent:
            pmsg = getattr(msg, msg.WhichOneof('data'))

            frame = Frame()
            frame.botId = pmsg.self_id
            frame.frame_type = Frame.FrameType.TSendGroupMsgReq
            frame.echo = ""
            frame.ok = True

            retmsg = SendGroupMsgReq()
            msgtext = Message()
            msgtext.type = "text"
            msgtext.data["text"] = 'qwq!'
            retmsg.message.append(msgtext)
            retmsg.group_id = pmsg.group_id
            retmsg.auto_escape = True
            frame.send_group_msg_req.CopyFrom(retmsg)

            data = frame.SerializeToString()
            await websocket.send_bytes(data)

def run_server(host:str  = 'localhost', port:int = 8082) -> None:
    uvicorn.run(app='pypbbot.server:app', host=host, port=port, reload=True, debug=True)
'''
    start_server = websockets.serve(main_logic, ip, port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
'''

