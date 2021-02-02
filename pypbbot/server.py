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
from pypbbot.log import logger

app = FastAPI()

drivers: Dict[int, Tuple[WebSocket, BaseDriver]] = {}
resp: Dict[str, Future] = {}

@app.on_event("startup")
async def init():
    logger.info('Hello, PyProtobufBot world!')


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
    if Frame.FrameType.Name(frame.frame_type).endswith('Event'):
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
    await ws.send_bytes(data)
    resp[frame.echo] = asyncio.get_event_loop().create_future()
    return await asyncio.wait_for(resp[frame.echo], 60)
    
from uvicorn.supervisors import Multiprocess
from uvicorn.server import Server
from uvicorn.config import Config
from pypbbot.utils import LoggableReload

def run_server(app, **kwargs):
    config = Config(app, **kwargs)
    server = Server(config=config)

    driver: BaseDriver = getattr(app, 'default_driver', BaseDriver)
    logger.info('Using driver: {}'.format(driver.__name__))
    logger.info('Start serving on {}:{}'.format(config.host, config.port))

    if (config.reload or config.workers > 1) and not isinstance(app, str):
        logger.warning("[app] should be an import string to enable 'reload' or 'workers'.")
        sys.exit(1)

    if config.should_reload:
        logger.info('Auto reloading has been enabled.')
        sock = config.bind_socket()
        supervisor = LoggableReload(config, target=server.run, sockets=[sock])
        supervisor.run()

    elif config.workers > 1:
        sock = config.bind_socket()
        supervisor = Multiprocess(config, target=server.run, sockets=[sock])
        supervisor.run()
    else:
        server.run()
