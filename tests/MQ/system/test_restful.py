import pytest
from httpx import AsyncClient
import httpx
import signal
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK
from InterviewMQ.Queue import router
# Create a FastAPI test application
app = FastAPI()
app.include_router(router)

client = TestClient(app)

@pytest.fixture
def mock_connected_clients(mocker):
    """Mock the connected_clients instance"""
    mock = mocker.patch("InterviewMQ.Queue.connected_clients", autospec=True)
    return mock

@pytest.mark.asyncio
async def test_publish(mock_connected_clients):
    """Test subscribing to a message queue"""
    payload = {
        'msg': 'Test',
        'topic': 'test_topic'
    }

    with client.stream("POST", "/interviewmq/publish", json=payload) as response:
        assert response.status_code == HTTP_200_OK

@pytest.mark.asyncio
async def test_wrong_uri(mock_connected_clients):
    """Test subscribing to a message queue"""
    payload = {
        'msg': 'Test',
        'topic': 'test_topic'
    }

    with client.stream("POST", "/interviewmq/test", json=payload) as response:
        assert response.status_code == 404
    

@pytest.mark.asyncio
async def test_no_topic(mock_connected_clients):
    """Test subscribing to a message queue"""
    payload = {
        'msg': 'Test'
    }

    with client.stream("POST", "/interviewmq/publish", json=payload) as response:
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_no_message(mock_connected_clients):
    """Test subscribing to a message queue"""
    payload = {
        'topic': 'test_topic'
    }

    with client.stream("POST", "/interviewmq/publish", json=payload) as response:
        assert response.status_code == 400
