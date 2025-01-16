from InterviewLIB.api import Consumer, ConnectionMethod
import asyncio
import pytest
import websockets
from unittest.mock import AsyncMock, patch, MagicMock

async def mock_server(websocket):
    """Simulate WebSocket server behavior."""
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")  # Simulated response
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed.")

async def start_mock_server():
    """Start WebSocket server on ws://localhost:8765."""
    server = await websockets.serve(mock_server, "localhost", 8765)
    await server.wait_closed()

@pytest.fixture(scope="module", autouse=True)
def run_mock_server():
    """Run the WebSocket mock server in the background before tests start."""
    loop = asyncio.get_event_loop()
    server_task = loop.create_task(start_mock_server())  # Start server
    yield  # Let tests run
    server_task.cancel()  # Stop server after tests

@pytest.mark.asyncio
async def test_run_ws_success():
    client = Consumer("ws://localhost:8765")
    client.subscribe("foo") 

@pytest.mark.asyncio
async def test_run_http_success():
    client = Consumer("http://localhost:8765")
    client.subscribe("foo") 

@pytest.mark.asyncio
async def test_run_http_wrong_url():
    client = Consumer("http://localhost:1111/test")
    client.subscribe("foo") 

@pytest.mark.asyncio
async def test_run_ws_wrong_url():
    client = Consumer("ws://localhost:1111/test")
    client.subscribe("foo") 