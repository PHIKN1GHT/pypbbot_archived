
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from pypbbot import app, logger
from pypbbot.protocol import PrivateMessageEvent, Frame
import uuid
import time

client = TestClient(app)


def test_connect() -> None:
    pass

# pytest -rP pypbbot_tests
# pytest -rx pypbbot_tests


def test_websocket() -> None:
    total_times = 50000
    logger.disable('pypbbot')
    with client.websocket_connect("/ws/") as ws:
        i = total_times
        time_start = time.time()
        while i > 0:
            event = PrivateMessageEvent()
            frame = Frame()
            frame.botId, frame.echo, frame.ok = 12305, "", True
            frame.frame_type = Frame.TPrivateMessageEvent
            frame.private_message_event.CopyFrom(event)
            data = frame.SerializeToString()
            ws.send_bytes(frame.SerializeToString())
            i -= 1
        time_cost = time.time() - time_start
        logger.debug('\n{} frames has been passed. \nTotal cost: {:.2f} seconds. \nProcessing speed: {:.2f} frames pre second.'.format(
            total_times, time_cost, total_times / time_cost))
        #assert data == {"msg": "Hello WebSocket"}
        #response = client.get("/api/help_center/detail", params={"pk": 1}, headers=get_headers())
        #assert response.status_code==200
