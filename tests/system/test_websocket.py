import pytest
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
        assert "Server response" in response

def test_subscribe_command():
    with client.websocket_connect("/interviewmq") as websocket:
        websocket.send_text(json.dumps({"command": "subscribe", "topic": "test_topic"}))
        response = websocket.receive_text()
        assert "Server response" in response

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
        assert "Server response" in response

def test_invalid_indicator():
    with client.websocket_connect("/interviewmq") as websocket:
        websocket.send_text(json.dumps({"invalid_indicator": "subscribe"}))
        response = websocket.receive_text()
        assert "Server response" in response

def test_non_json():
    with client.websocket_connect("/interviewmq") as websocket:
        websocket.send_text("'command': 'subscribe'")
        response = websocket.receive_text()
        assert "Server response" in response

def test_timeout_handling():
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/interviewmq") as websocket:
            # Simulate no activity to trigger timeout
            pass
