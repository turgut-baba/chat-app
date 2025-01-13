from typing import Callable, Union
import websockets
import asyncio
import json
import httpx
from .Settings import ConnectionMethod
from .Communicator import Communicator

class Consumer(Communicator):

    def __init__(self, url):
        super().__init__(url)


    async def subscribe(self, topic):
        """Start the WebSocket client."""
        await self.run(topic)

    async def run_http(self, topic):
        url = "http://localhost:8000/interviewmq/subscribe"

        payload = {
            "topic": "foo",
        }
        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", url, json=payload, headers=headers) as response:
                    if response.status_code != 200:
                        print(f"Failed to subscribe: {response.status_code}")
                        return
                    
                    print("Subscribed successfully. Listening for messages...")
                    async for line in response.aiter_lines():
                        try:
                            if line: 
                                ... # Skip keep-alive newlines
                            if line.startswith("data:"):
                                message = line[5:].strip()  # Remove "data:" prefix
                                print(f"Received message: {message}")
                        except Exception as e:
                            print(f"Inner error: {e}")
            except Exception as e:
                print(f"Error occurred: {e}")


    async def run_ws(self, topic):
        """Connect to the WebSocket and listen for messages."""
        try:
            async with websockets.connect(self.url) as websocket:
                self.websocket = websocket

                # Subscribe to the topic
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

                # Listen for messages
                while True:
                    try:
                        data = await websocket.recv()

                        if not self.has_filter:
                            print(data)
                        elif self.check_filter(data):
                            print(data)
                        else:
                            continue
                            
                    except asyncio.TimeoutError:
                        print("Timeout: No message received within 30 seconds.")
                        break
                    except json.JSONDecodeError:
                        print("Invalid JSON received.")
                        break
        except Exception as e:
            print(f"Error: {e}")

