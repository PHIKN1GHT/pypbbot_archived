import sys, os
import uvicorn

from fastapi import FastAPI, WebSocket

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
@app.websocket("/ws/test/")
async def recv_frame(websocket: WebSocket):
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
        if frame.WhichOneof('data'): # Permitting APIResp
            await driver.handle(getattr(frame, frame.WhichOneof('data')))

async def send_frame(driver, api_content):
    frame = Frame()
    ws, _ = drivers[driver.botId]
    frame.botId, echo, ok = driver.botId, '', True
    try:
        frame.frame_type = getattr(Frame.FrameType, 'T' + type(api_content).__name__)
        getattr(frame, in_lower_case(type(api_content).__name__)).CopyFrom(api_content)
        data = frame.SerializeToString()
        await ws.send_bytes(data)
    finally:
        pass

def run_server(**kwargs):
    uvicorn.run(**kwargs)
