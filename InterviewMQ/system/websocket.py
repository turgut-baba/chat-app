from fastapi import APIRouter, HTTPException, WebSocket
from pydantic import BaseModel
from InterviewMQ.util.logger import Logger
import asyncio
from InterviewMQ.Queue import connected_clients, topics

import json

router = APIRouter()

logger = Logger("server.log", "InterviewMQ")

# WebSocket Endpoint for real-time communication and front-end services.
@router.websocket("/interviewmq")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_address = websocket.client
    logger.log(f"Client connected: {client_address}")
    connected_clients.append(client_address)
    try:
        while True:
            try:
                data = await websocket.receive_text()  # Timeout after 30 seconds
                message = json.loads(data)
                logger.log(f"Message received from {client_address}: {data}")

                if message.get("command") == "subscribe":
                    topics[message.get("topic")].append(websocket)
                elif message.get("command") == "publish":
                    all_subscribed = topics[message.get("topic")]
                    for reciever in all_subscribed:
                        msg = message.get("msg")
                        await reciever.send_text(msg)
                
                await websocket.send_text(f"Server response: Recieved message!")
            except asyncio.TimeoutError:
                connected_clients.remove(client_address)
                logger.log(f"Timeout, closing connection with {client_address}")
                break
    except Exception as e:
        connected_clients.clear()
        logger.log(f"Connection closed: {e}") 