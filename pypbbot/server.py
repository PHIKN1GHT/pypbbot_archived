import os, sys
import uvicorn # type: ignore
import asyncio
import uuid

from fastapi import FastAPI, WebSocket, BackgroundTasks
from typing import Tuple, Dict
from asyncio import Future

from pypbbot.driver import BaseDriver
from pypbbot.utils import in_lower_case
from pypbbot.types import ProtobufBotAPI
from pypbbot.types import ProtobufBotFrame as Frame
from pypbbot.types import ProtobufBotMessage as Message
from pypbbot.log import logger, LOG_CONFIG
from pypbbot.plugin import load_plugins

app = FastAPI()

drivers: Dict[int, Tuple[WebSocket, BaseDriver]] = {}
resp: Dict[str, Future] = {}

@app.on_event("startup")
async def init():
    if (hasattr(app, 'plugin_path')):
        load_plugins(getattr(app, 'plugin_path'))
    logger.info('Everything is almost ready. Hello, PyProtobufBot world!')

@app.on_event("shutdown")
async def close():
    logger.info('Shutting down. Have a nice day!')

@app.websocket("/ws/test/")
async def handle_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    logger.info('Accepted client from {}:{}'.format(websocket.client.host, websocket.client.port))
    while True:
        rawdata: bytes = await websocket.receive_bytes()
        frame = Frame()
        frame.ParseFromString(rawdata)
        if not frame.botId in drivers.keys():
            if not hasattr(app, 'default_driver'):
                setattr(app, 'default_driver', BaseDriver)
                getattr(app, 'default_driver')
            drivers[frame.botId] = (websocket, getattr(app, 'default_driver')(frame.botId))
        else:
            _, dri = drivers[frame.botId]
            drivers[frame.botId] = (websocket, dri)

        ws, driver = drivers[frame.botId]
        asyncio.create_task(recv_frame(frame, driver))

async def recv_frame(frame: Frame, driver: BaseDriver) -> None:
    frame_type = Frame.FrameType.Name(frame.frame_type)
    logger.debug('Recv frame [{}] from client [{}]'.format(frame_type, frame.botId))
    if frame_type.endswith('Event'):
        await driver.handle(getattr(frame, frame.WhichOneof('data')))
    else:
        if frame.echo in resp.keys():
            if isinstance(frame.WhichOneof('data'), str):
                resp[frame.echo].set_result(getattr(frame, frame.WhichOneof('data')))
            else:
                resp[frame.echo].set_result(None)

async def send_frame(driver: BaseDriver, api_content: ProtobufBotAPI) -> ProtobufBotAPI:
    frame = Frame()
    ws, _ = drivers[driver.botId]
    frame.botId, frame.echo, frame.ok = driver.botId, str(uuid.uuid1()), True
    frame.frame_type = getattr(Frame.FrameType, 'T' + type(api_content).__name__)
    getattr(frame, in_lower_case(type(api_content).__name__)).CopyFrom(api_content)
    data = frame.SerializeToString()
    frame_type = Frame.FrameType.Name(frame.frame_type)
    logger.debug('Send frame [{}] to client [{}]'.format(frame_type, frame.botId))
    await ws.send_bytes(data)
    resp[frame.echo] = asyncio.get_event_loop().create_future()
    return await asyncio.wait_for(resp[frame.echo], 60)

def run_server(**kwargs): # type: ignore
    uvicorn.run(log_config = LOG_CONFIG, **kwargs)
