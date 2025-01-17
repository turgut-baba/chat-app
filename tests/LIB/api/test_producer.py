import pytest
from unittest.mock import AsyncMock, patch, MagicMock 
import json
import websockets
from InterviewLIB.api import Producer, ConnectionMethod
import subprocess
import time
import httpx

server_port = 5050
command = "uvicorn InterviewMQ:app --host 0.0.0.0 --port " + str(server_port) + " --reload"
subprocess.Popen(["start", "cmd", "/c", command], shell=True)
time.sleep(3)

@pytest.mark.asyncio
async def test_run_success():
    client = Producer("ws://localhost:5050/interviewmq") 

    topic = "test_topic"
    message = "test_message"
    
    response = await client.run(topic, message)
    
    assert "Success" in response 


@pytest.mark.asyncio
async def test_run_ws_success():
    client = Producer("ws://localhost:5050/interviewmq") 

    topic = "test_topic"
    message = "test_message"
    
    response = await client.run_ws(topic, message)
    
    assert "Success" in response 

@pytest.mark.asyncio
async def test_run_http_success():
    client = Producer("http://localhost:5050/interviewmq") 

    topic = "test_topic"
    message = "test_message"
    
    response = await client.run_http(topic, message)
    
    assert "Message sent to subscribers" == response['status'] 

@pytest.mark.asyncio
async def test_run_set_client():
    client = Producer("http://localhost:5050/interviewmq") 

    topic = "test_topic"
    message = "test_message"

    client.set_connection(ConnectionMethod.HTTP)
    
    response = await client.run(topic, message)
    
    assert "Message sent to subscribers" == response['status']

@pytest.mark.asyncio
async def test_run_ws_filter_string_success():
    client = Producer("ws://localhost:5050/interviewmq") 

    topic = "test_topic"
    message = "test message"

    client.set_filter("test")
    
    response = await client.run_ws(topic, message)
    
    assert "Success" in response 

@pytest.mark.asyncio
async def test_run_ws_filter_success():
    client = Producer("ws://localhost:5050/interviewmq") 

    topic = "test_topic"
    message = "test message"

    filter = lambda x: True if "test" in x else False

    client.set_filter(filter)
    
    response = await client.run_ws(topic, message)
    
    assert "Success" in response 

@pytest.mark.asyncio
async def test_run_ws_wrong_url():
    client = Producer("ws://none:0000/") 

    topic = "test_topic"
    message = "test message"

    client.set_retries(5)

    with pytest.raises(Exception) as context:
        response = await client.run_ws(topic, message)

@pytest.mark.asyncio
async def test_run_ws_wrong_uri():
    client = Producer("ws://localhost:5050/test") 

    topic = "test_topic"
    message = "test message"

    client.set_retries(5)

    with pytest.raises(Exception) as context:
        response = await client.run_ws(topic, message)

@pytest.mark.asyncio
async def test_run_http_wrong_url():
    client = Producer("ws://none:0000/") 

    topic = "test_topic"
    message = "test message"

    client.set_retries(5)

    with pytest.raises(httpx.ConnectError) as context:
        response = await client.run_http(topic, message)

@pytest.mark.asyncio
async def test_run_http_wrong_uri():
    client = Producer("ws://localhost:5050/test") 

    topic = "test_topic"
    message = "test message"

    client.set_retries(5)

    with pytest.raises(Exception) as context:
        response = await client.run_http(topic, message)

@pytest.mark.asyncio
async def test_run_ws_retries():
    client = Producer("ws://none:0000/") 

    topic = "test_topic"
    message = "test message"

    client.set_retries(5)

    with pytest.raises(Exception) as context:
        response = await client.run(topic, message)
