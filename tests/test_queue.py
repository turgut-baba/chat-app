from InterviewMQ.Queue import *

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, WebSocket
import asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_websocket_connection():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        async with client.websocket_connect("/interviewmq") as websocket:
            # Test connection
            await websocket.send_text("Hello Server!")
            response = await websocket.receive_text()
            assert response == "Server response: Hello Server!"


@pytest.mark.asyncio
async def test_websocket_timeout():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        async with client.websocket_connect("/interviewmq") as websocket:
            # Do not send any data, wait for timeout
            try:
                await asyncio.sleep(35)  # Exceed the 30s timeout
                response = await websocket.receive_text()
            except Exception as e:
                assert "Timeout" in str(e)


@pytest.mark.asyncio
async def test_websocket_multiple_messages():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        async with client.websocket_connect("/interviewmq") as websocket:
            messages = ["Message 1", "Message 2", "Message 3"]
            for msg in messages:
                await websocket.send_text(msg)
                response = await websocket.receive_text()
                assert response == f"Server response: {msg}"
