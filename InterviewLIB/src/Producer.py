import asyncio
from InterviewLIB.api.Producer import Producer 
import websockets
import json

class ProducerImpl(Producer):
    def __init__(self, uri):
        self.uri = uri

    async def send_message(self, topic, message):
        message = {
                "command": "publish",
                "topic": topic,
                "msg": message
            }
        try:
            async with websockets.connect(self.uri) as websocket:
                # Send a message to the server
                await websocket.send(json.dumps(message))
                print("Message sent to server.")
                
                # Receive a response from the server
                response = await websocket.recv()
                print(f"Server response: {response}")
        except Exception as e:
            print(f"WebSocket connection failed: {e}")

    def publish(self, message, topic):
        asyncio.run(self.send_message(message, topic))
