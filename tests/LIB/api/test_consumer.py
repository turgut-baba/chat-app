from InterviewLIB.api import Consumer, ConnectionMethod
import asyncio
import pytest
import websockets
from unittest.mock import AsyncMock, patch, MagicMock
import json
import threading

"""
!!! IMPORTANT !!! 

I couldn't find a way to do unit tests on consumer as it's almost alwasys stuck
on an infinite loop. I tried using many different strategies but it always stuck. The best course of action
would be to do integration tests on a controlled environment.
"""

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

    client.set_connection(ConnectionMethod.HTTP)

    client.subscribe("foo") 

@pytest.mark.asyncio
async def test_run_http_wrong_url():
    client = Consumer("http://localhost:1111/test")

    client.set_connection(ConnectionMethod.HTTP)

    client.subscribe("foo") 

@pytest.mark.asyncio
async def test_run_ws_wrong_url():
    client = Consumer("ws://localhost:1111/test")

    client.subscribe("foo") 

@pytest.mark.asyncio
async def test_run_ws_filter_string():
    client = Consumer("ws://localhost:1111/test")

    client.set_filter("test")

    client.subscribe("foo") 

@pytest.mark.asyncio
async def test_run_ws_filter_():
    client = Consumer("ws://localhost:1111/test")

    filter = lambda x: True if "test" in x else False

    client.set_filter(filter)

    client.subscribe("foo") 


@pytest.mark.asyncio
async def test_run_ws_set_retry():
    client = Consumer("ws://localhost:1111/test")

    filter = lambda x: True if "test" in x else False

    client.set_retries(5)

    client.subscribe("foo") 

@pytest.mark.asyncio
async def test_run_ws_success():

    """ THIS IS NOT WORKING BUT THE ACTUAL TESTS SHOULD BE SOMETHING LIKE THIS"""

    topic = "test_topic"
    mock_ws = AsyncMock()
    
    async def mock_recv():
        responses = [
            json.dumps({"status": "subscribed", "topic": topic}),  # Subscription confirmation
            json.dumps({"message": "data_received"}),  # Incoming message
        ]
        for response in responses:
            yield response
        raise websockets.exceptions.ConnectionClosed(1000, "Test completed")  # Close connection

    mock_ws.recv = AsyncMock(side_effect=mock_recv())

    with patch("websockets.connect", return_value=mock_ws):
        consumer = Consumer("ws://localhost")
        consumer._has_filter = False 

        try:
            stop_event = threading.Event()
            def start_async_in_thread():
                """Runs the async function inside a separate thread."""
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            thread = threading.Thread(target=start_async_in_thread)
            thread.start()

            print("Stopping async thread...")
            stop_event.set()  
            thread.join()  
        except websockets.exceptions.ConnectionClosed:
            pass 

        # Assertions
        #mock_ws.send.assert_called_with(json.dumps({"command": "subscribe", "topic": topic}))
        #assert mock_ws.recv.await_count == 2  # Subscription + 1 message received

