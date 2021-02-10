import os, sys, asyncio, uuid, inspect
import uvicorn # type: ignore

from fastapi import FastAPI, WebSocket, BackgroundTasks
from typing import Tuple, Dict, Callable, Awaitable, Union
from asyncio import Future

from pypbbot.driver import BaseDriver, AffairDriver, Drivable
from pypbbot.utils import in_lower_case, LRULimitedDict, Clips
from pypbbot.typing import ProtobufBotAPI, ProtobufBotFrame as Frame, ProtobufBotMessage as Message, ProtobufBotEvent as Event, LoadingEvent, UnloadingEvent
from pypbbot.logging import logger, LOG_CONFIG
from pypbbot.plugin import load_plugins
from pypbbot.protocol import SendPrivateMsgReq, PrivateMessageEvent, GroupMessageEvent, SendGroupMsgReq

from starlette.websockets import WebSocketDisconnect

app = FastAPI()

drivers: LRULimitedDict[int, Tuple[WebSocket, Drivable]] = LRULimitedDict()
resp_cache: LRULimitedDict[str, Future] = LRULimitedDict()

@app.on_event("startup")
async def init():
    global loop
    loop = asyncio.get_running_loop()
    if (hasattr(app, 'plugin_path')):
        await load_plugins(getattr(app, 'plugin_path'))
    logger.info('Everything is almost ready. Hello, PyProtobufBot world!')
    await AffairDriver().handle(LoadingEvent())

@app.on_event("shutdown")
async def close():
    logger.info('Shutting down. Have a nice day!')
    await AffairDriver().handle(UnloadingEvent())
    
@app.websocket("/ws/test/")
async def handle_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    logger.info('Accepted client from {}:{}'.format(websocket.client.host, websocket.client.port))
    while True:
        try:
            rawdata: bytes = await websocket.receive_bytes()
            frame = Frame()
            frame.ParseFromString(rawdata)

            if not frame.botId in drivers.keys():
                if not hasattr(app, 'driver_builder'):
                    setattr(app, 'driver_builder', BaseDriver)
                driver_builder = getattr(app, 'driver_builder')

                if inspect.isclass(driver_builder):
                    drivers[frame.botId] = (websocket, driver_builder(frame.botId))
                else:
                    drivers[frame.botId] = (websocket, await driver_builder(frame.botId))
            else:
                _, dri = drivers[frame.botId]
                drivers[frame.botId] = (websocket, dri)
            await recv_frame(frame, frame.botId)
        except WebSocketDisconnect:
            logger.warning('Connection to {} has been closed.'.format(websocket.client.host))
            break
        #asyncio.create_task(recv_frame(frame, frame.botId))

async def recv_frame(frame: Frame, botId: int) -> None:
    frame_type = Frame.FrameType.Name(frame.frame_type)
    logger.debug('Recv frame [{}] from client [{}]'.format(frame_type, frame.botId))
    _, driver = drivers[frame.botId]
    if frame_type.endswith('Event'):
        event = getattr(frame, frame.WhichOneof('data'))
        #if isinstance(event, PrivateMessageEvent):
        #    print(event.raw_message)
        if isinstance(driver, BaseDriver):
            #await driver.handle(event)
            asyncio.create_task(driver.handle(event))
        else: # Support for Functional Driver Builder
            #await driver(event)
            asyncio.create_task(driver(event))
    else:
        if frame.echo in resp_cache.keys():
            if isinstance(frame.WhichOneof('data'), str):
                resp_cache[frame.echo].set_result(getattr(frame, frame.WhichOneof('data')))
            else:
                resp_cache[frame.echo].set_result(None)

async def send_frame(botId: int, api_content: ProtobufBotAPI) -> ProtobufBotAPI:
    frame = Frame()
    ws, _ = drivers[botId]
    frame.botId, frame.echo, frame.ok = botId, str(uuid.uuid1()), True
    frame.frame_type = getattr(Frame.FrameType, 'T' + type(api_content).__name__)
    getattr(frame, in_lower_case(type(api_content).__name__)).CopyFrom(api_content)
    data = frame.SerializeToString()
    frame_type = Frame.FrameType.Name(frame.frame_type)
    logger.debug('Send frame [{}] to client [{}]'.format(frame_type, frame.botId))
    await ws.send_bytes(data)
    resp_cache[frame.echo] = asyncio.get_event_loop().create_future()

    try:
        retv = await asyncio.wait_for(resp_cache[frame.echo], 60)
    except asyncio.TimeoutError:
        logger.error('Timed out for frame [{}]'.format(frame.echo))
        retv = None
    finally:
        resp_cache.remove(frame.echo)
    return retv

'''
async def sendPrivateTo(botId: int, user_id: int, clips: Clips):
    api_content = SendPrivateMsgReq()
    api_content.user_id, auto_escape = user_id, True
    api_content.message.extend(clips.toMessageList())
    return await send_frame(botId, api_content)
'''

def run_server(**kwargs): # type: ignore
    uvicorn.run(loop="asyncio", log_config = LOG_CONFIG, **kwargs)

import queue
from queue import Queue