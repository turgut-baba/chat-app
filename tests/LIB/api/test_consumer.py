from InterviewLIB.api import Consumer, ConnectionMethod
import asyncio
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.fixture
def consumer():
    """Fixture to create a Consumer instance."""
    return Consumer("ws://testserver")

@pytest.mark.asyncio
async def test_run_http_success(consumer, mocker):
    """Test HTTP subscription successfully receives messages."""
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.aiter_lines.return_value = iter(["data: message_1", "data: message_2"])

    mocker.patch("httpx.AsyncClient.stream", new_callable=AsyncMock)
    mock_client.stream.return_value.__aenter__.return_value = mock_response
    mocker.patch("httpx.AsyncClient", return_value=mock_client)

    consumer.set_connection(ConnectionMethod.HTTP)

    await consumer.run("test_topic")
