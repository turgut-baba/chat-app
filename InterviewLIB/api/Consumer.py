import websockets
import json
import httpx
from .Communicator import Communicator

class Consumer(Communicator):

    def __init__(self, url):
        super().__init__(url)

    async def subscribe(self, topic):
        """Start the WebSocket client."""
        await self.run(topic)

    async def run_http(self, topic):
        payload = {
            "topic": topic,
        }

        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=None) as client:
            try:
                async with client.stream("POST", self._url + "/subscribe", json=payload, headers=headers) as response:
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
                raise Exception(f"Error occurred: {e}")


    async def run_ws(self, topic):
        try:
            async with websockets.connect(self._url) as websocket:
                self._websocket = websocket

                """Subscribe to a topic."""
                if not self._websocket:
                    raise RuntimeError("WebSocket connection is not established. Call 'run' first.")

                subscription = {
                    "command": "subscribe",
                    "topic": topic
                }
                await self._websocket.send(json.dumps(subscription))
                print(f"Sent: {subscription}")

                # Wait for subscription confirmation
                response = await self._websocket.recv()
                print(f"Server Response: {response}")

                # Listen for messages on the subscribed topic
                while True:
                    try:
                        data = await self._websocket.recv()

                        if not self._has_filter:
                            print(data) # The end result, we simply print it as there is no front-end for this.
                        elif self.check_filter(data):
                            print(data)
                        
                    except json.JSONDecodeError:
                        print("Invalid JSON received.")
        except Exception as e:
            if "1012" in str(e):
                print("Received 1012 error, performing service restart.")
                await self.restart_service()
                await self.run_ws(topic)
            else: 
                raise Exception(f"There has been an error in websocket consumer: {e}")
