import websockets
import json
import httpx
from .Communicator import Communicator

class Producer(Communicator):
    def __init__(self, uri):
        super().__init__(uri)

    async def publish(self, topic, message):
        return await self.run(topic, message)

    async def run_ws(self, topic, message):
        message = {
                "command": "publish",
                "topic": topic,
                "msg": message
            }
        try:
            async with websockets.connect(self._url) as websocket:
                if not self._has_filter:
                    await websocket.send(json.dumps(message))
                    print("Message sent to server.")
                elif self.check_filter(message['msg']):
                    await websocket.send(json.dumps(message))
                    print("Message sent to server.")
                else:
                    print('Message does not fit filter criterias.')
                
                response = await websocket.recv()
                print(f"Server response: {response}")
                return response
        except Exception as e:
            raise Exception(f"WebSocket connection failed: {e}")
        
    async def run_http(self, topic, message):
        payload = {
            "topic": topic,
            "msg": message
        }
        headers = {
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self._url, json=payload, headers=headers)

            if response.status_code != 200:
                raise Exception(f"Network response was not ok: {response.status_code}, {response.text}")

            return response.json()
