from fastapi import Request, HTTPException, WebSocket
from pydantic import BaseModel
from InterviewMQ.util.logger import Logger
from InterviewMQ.util.status import Status
import asyncio
from InterviewMQ.Queue import connected_clients, topics, router

import json

logger = Logger("server.log", "InterviewMQ")

# WebSocket Endpoint for real-time communication and front-end services.
@router.websocket("/interviewmq")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    client_address = websocket.client
    logger.log(f"Client connected: {client_address}")
    #connected_clients.append(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()  # Timeout after 30 seconds
                message = json.loads(data)
                logger.log(f"Message received from {client_address}: {data}")

                if message.get("command") == "subscribe":
                    await connected_clients.add_websocket_connection(message.get("topic"), websocket)

                elif message.get("command") == "publish":
                    await connected_clients.broadcast(message.get("topic"), message.get("msg"))
                
                await websocket.send_text(f"Success: {Status.SUCCESS.value}")
            except asyncio.TimeoutError:
                connected_clients.remove(message['topic'], websocket)
                logger.log(f"Timeout, closing connection with {client_address}")
                break
    except Exception as e:
        #connected_clients.clear()
        logger.log(f"Connection closed: {e}") 
