from InterviewMQ.system.message import ConnectionManager
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from starlette.websockets import WebSocket
from collections import defaultdict

@pytest.fixture
def connection_manager():
    """Fixture to create a fresh ConnectionManager instance for each test."""
    return ConnectionManager()

@pytest.mark.asyncio
async def test_add_remove_websocket_connection(connection_manager):
    """Test adding and removing WebSocket connections."""
    topic = "test_topic"
    websocket = AsyncMock(spec=WebSocket)

    # Add WebSocket connection
    await connection_manager.add_websocket_connection(topic, websocket)
    assert websocket in connection_manager.websocket_connections[topic]

    # Remove WebSocket connection
    await connection_manager.remove_websocket_connection(topic, websocket)
    assert websocket not in connection_manager.websocket_connections[topic]


@pytest.mark.asyncio
async def test_add_remove_sse_connection(connection_manager):
    """Test adding and removing SSE queues."""
    topic = "test_topic"
    queue = asyncio.Queue()

    # Add SSE connection
    await connection_manager.add_sse_connection(topic, queue)
    assert queue in connection_manager.sse_queues[topic]

    # Remove SSE connection
    await connection_manager.remove_sse_connection(topic, queue)
    assert queue not in connection_manager.sse_queues[topic]


@pytest.mark.asyncio
async def test_broadcast_message_to_websockets(connection_manager):
    """Test broadcasting messages to WebSocket clients."""
    topic = "test_topic"
    websocket = AsyncMock(spec=WebSocket)

    # Add WebSocket connection
    await connection_manager.add_websocket_connection(topic, websocket)

    # Broadcast a message
    message = "Hello, WebSockets!"
    await connection_manager.broadcast(topic, message)

    # Ensure WebSocket received the message
    websocket.send_text.assert_called_once_with(message)


@pytest.mark.asyncio
async def test_broadcast_message_to_sse(connection_manager):
    """Test broadcasting messages to SSE clients."""
    topic = "test_topic"
    queue = asyncio.Queue()

    # Add SSE connection
    await connection_manager.add_sse_connection(topic, queue)

    # Broadcast a message
    message = "Hello, SSE!"
    await connection_manager.broadcast(topic, message)

    # Ensure SSE client received the message
    received_message = await queue.get()
    assert received_message == message


@pytest.mark.asyncio
async def test_broadcast_removes_failed_websockets(connection_manager):
    """Test that failed WebSocket clients are removed from the connection manager."""
    topic = "test_topic"
    websocket = AsyncMock(spec=WebSocket)

    # Simulate WebSocket failing when sending a message
    websocket.send_text.side_effect = Exception("WebSocket failure")

    await connection_manager.add_websocket_connection(topic, websocket)

    # Broadcast a message (this should trigger removal of the failed WebSocket)
    message = "Test Message"
    await connection_manager.broadcast(topic, message)

    # Ensure the WebSocket was removed after failure
    assert websocket not in connection_manager.websocket_connections[topic]

@pytest.mark.asyncio
async def test_clear_connections(connection_manager):
    """Test clearing all WebSocket and SSE connections."""
    topic = "test_topic"
    websocket = AsyncMock(spec=WebSocket)
    queue = asyncio.Queue()

    await connection_manager.add_websocket_connection(topic, websocket)
    await connection_manager.add_sse_connection(topic, queue)

    # Ensure connections exist
    assert connection_manager.websocket_connections[topic]
    assert connection_manager.sse_queues[topic]

    # Clear all connections
    await connection_manager.clear()

    # Ensure all connections are removed
    assert connection_manager.websocket_connections == defaultdict(list)
    assert connection_manager.sse_queues == defaultdict(list)