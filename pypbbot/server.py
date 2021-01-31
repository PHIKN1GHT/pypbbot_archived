import sys, os
import uvicorn, asyncio
import uuid

from fastapi import FastAPI, WebSocket, BackgroundTasks

from pypbbot import protocol
from pypbbot.protocol import Frame
from pypbbot.protocol import PrivateMessageEvent, GroupMessageEvent
from pypbbot.protocol import SendPrivateMsgReq, SendGroupMsgReq
from pypbbot.protocol import Message

from pypbbot.driver import BaseDriver as base_driver
from pypbbot.utils import in_lower_case

app = FastAPI()

def api_check():
    for entry in protocol.__dict__:
        if entry.endswith('Req') or entry.endswith('Resp') or entry.endswith('Event'):
            assert getattr(Frame.FrameType, 'T' + entry) != None

drivers = {}
resp = {}

@app.websocket("/ws/test/")
async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        rawdata = await websocket.receive_bytes()
        frame = Frame()
        frame.ParseFromString(rawdata)
        if not frame.botId in drivers.keys():
            if not hasattr(app, 'default_driver'):
                app.default_driver = base_driver
            drivers[frame.botId] = (websocket, app.default_driver(frame.botId))
        else:
            _, dri = drivers[frame.botId]
            drivers[frame.botId] = (websocket, dri)

        ws, driver = drivers[frame.botId]
        asyncio.create_task(recv_frame(frame, driver))

async def recv_frame(frame, driver):
    if Frame.FrameType.Name(frame.frame_type).endswith('Event'):
        await driver.handle(getattr(frame, frame.WhichOneof('data')))
    else:
        if frame.echo in resp.keys():
            resp[frame.echo].set_result(getattr(frame, frame.WhichOneof('data')))

async def send_frame(driver, api_content):
    frame = Frame()
    ws, _ = drivers[driver.botId]
    frame.botId, frame.echo, frame.ok = driver.botId, str(uuid.uuid1()), True
    frame.frame_type = getattr(Frame.FrameType, 'T' + type(api_content).__name__)
    getattr(frame, in_lower_case(type(api_content).__name__)).CopyFrom(api_content)
    data = frame.SerializeToString()
    await ws.send_bytes(data)
    resp[frame.echo] = asyncio.get_event_loop().create_future()
    return await asyncio.wait_for(resp[frame.echo], 60)
    
def run_server(**kwargs):
    uvicorn.run(**kwargs)
