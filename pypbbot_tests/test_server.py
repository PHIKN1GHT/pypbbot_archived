
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from pypbbot import app

def test_websocket():
    client = TestClient(app)

