from fastapi import Request, HTTPException, WebSocket
from pydantic import BaseModel
from InterviewMQ.util.status import Status
import asyncio
from fastapi import WebSocketDisconnect
from InterviewMQ.Queue import connected_clients, router

import json
from json import JSONDecodeError

@router.websocket("/interviewmq")
async def websocket_endpoint(websocket: WebSocket):

    """ Websocket endpoint. This function does not have a timeout so that 
    subscribers can stay connected. Mainly uses functionality from ConnectedClients
    defined in Queue.py"""

    await websocket.accept()

    print(f"Client connected: {websocket.client}")

    message = ""
    
    try:
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                print(f"Message received from {websocket.client}: {data}")

                if 'command' not in message:
                    await websocket.send_text(f"Error, command not found: {Status.FAIL.value}, there must be a command.")

                if message.get("command") == "subscribe":
                    await connected_clients.add_websocket_connection(message.get("topic"), websocket)

                elif message.get("command") == "publish":
                    await connected_clients.broadcast(message.get("topic"), message.get("msg"))
                
                else:
                    await websocket.send_text(f"Error, invalid command: {Status.FAIL.value}")
  
                await websocket.send_text(f"Success: {Status.SUCCESS.value}")
            except asyncio.TimeoutError:
                connected_clients.remove_websocket_connection(message.get("topic"), websocket)
                print(f"Timeout, closing connection with {websocket.client}")
                break
            except JSONDecodeError as je:
                await websocket.send_text(f"Error, invalid format, must be json: {Status.FAIL.value}")
    except WebSocketDisconnect as disconnect:
        if message is not "" and message.get("command") == "subscribe":
            await connected_clients.remove_websocket_connection(message.get("topic"), websocket)
    except Exception as e:
        await connected_clients.clear()
        raise(Exception(f"Server error: {e}")) 

