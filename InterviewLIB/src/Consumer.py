from InterviewLIB.api.Consumer import Consumer
from typing import Callable
import websockets
import asyncio
import json

class ConsumerImpl(Consumer):

    def __init__(self, url):
        self.url = url
        self.websocket = None

    async def subscribe_to_server(self, topic):
        """Subscribe to a topic."""
        if not self.websocket:
            raise RuntimeError("WebSocket connection is not established. Call 'run' first.")

        subscription = {
            "command": "subscribe",
            "topic": topic
        }
        await self.websocket.send(json.dumps(subscription))
        print(f"Sent: {subscription}")

        # Wait for subscription confirmation
        response = await self.websocket.recv()
        print(f"Server Response: {response}")


    def subscribe(self, topic):
        """Start the WebSocket client."""
        asyncio.run(self.run(topic))

    async def run(self, topic):
        """Connect to the WebSocket and listen for messages."""
        try:
            async with websockets.connect(self.url) as websocket:
                self.websocket = websocket

                # Subscribe to the topic
                await self.subscribe_to_server(topic)

                # Listen for messages
                while True:
                    try:
                        data = await websocket.recv()
                        print(data)
                    except asyncio.TimeoutError:
                        print("Timeout: No message received within 30 seconds.")
                        break
                    except json.JSONDecodeError:
                        print("Invalid JSON received.")
                        break
        except Exception as e:
            print(f"Error: {e}")


    def filter_messages(self, message, criteria):
        return super().filter_messages(message, criteria)

