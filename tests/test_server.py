
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from pypbbot import app

def test_websocket():
    client = TestClient(app)
    #with client.websocket_connect("/ws/test/") as websocket:
    #    data = websocket.receive_json()
    #    assert data == {"msg": "Hello WebSocket"}


