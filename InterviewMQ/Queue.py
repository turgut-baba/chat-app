from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from typing import List

app = FastAPI()

# In-memory message queue
message_queue = asyncio.Queue()

# Store connected WebSocket clients
connected_clients: List[WebSocket] = []

@app.websocket("/interviewmq")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected!")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message received: {data}")
            await websocket.send_text(f"Server response: {data}")
    except Exception as e:
        print(f"Connection closed: {e}")