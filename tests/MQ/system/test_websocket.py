import pytest
import asyncio
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from InterviewMQ.system.websocket import *
from InterviewMQ import app
import json
# WebSocket test client
client = TestClient(app)

def test_websocket_connection():
    with client.websocket_connect("/interviewmq") as websocket:
        assert websocket is not None
        websocket.send_text(json.dumps({"command": "subscribe", "topic": "test_topic"}))
        response = websocket.receive_text()

        assert "Success" in response and "100" in response

        websocket.send_text(json.dumps({"command": "publish", "topic": "test_topic", "msg": "Test"}))
        response = websocket.receive_text()

        assert "Test" in response

def test_subscribe_command():
    with client.websocket_connect("/interviewmq") as websocket:
        websocket.send_text(json.dumps({"command": "subscribe", "topic": "test_topic"}))
        response = websocket.receive_text()
        assert "Success" in response and "100" in response

def test_publish_command():
    with client.websocket_connect("/interviewmq") as websocket1:
        websocket1.send_text(json.dumps({"command": "subscribe", "topic": "test_topic"}))
        websocket1.receive_text()  # Consume the server response

        with client.websocket_connect("/interviewmq") as websocket2:
            websocket2.send_text(json.dumps({"command": "publish", "topic": "test_topic", "msg": "Hello, World!"}))
            websocket2.receive_text()  # Consume the server response

            # Verify that the first websocket receives the published message
            response = websocket1.receive_text()
            assert response == "Hello, World!"

def test_invalid_command():
    with client.websocket_connect("/interviewmq") as websocket:
        websocket.send_text(json.dumps({"command": "invalid_command"}))
        response = websocket.receive_text()
        assert "invalid command" in response and "400" in response

def test_invalid_indicator():
    with client.websocket_connect("/interviewmq") as websocket:
        websocket.send_text(json.dumps({"invalid_indicator": "subscribe"}))
        response = websocket.receive_text()
        assert "command not found" in response and "400" in response

@pytest.mark.asyncio
async def test_non_json():
    with client.websocket_connect("/interviewmq") as websocket:
        websocket.send_text("'command': 'subscribe'")
        response = websocket.receive_text()
        websocket.close()
        assert "invalid format" in response and "400" in response

@pytest.mark.asyncio
async def test_wrong_uri():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/interviewlib") as websocket:
            ...

@pytest.mark.asyncio
async def test_websocket_forced_disconnect():
    with client.websocket_connect("/interviewmq") as websocket:
        websocket.close()

