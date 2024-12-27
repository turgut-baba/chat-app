from abc import ABC, abstractmethod
from typing import Callable
from InterviewMQ.util.status import Status

class Consumer(ABC):
    def __init__(self, amqp_url):
        self.amqp_url = amqp_url

    async def on_message(self, message):
        async with message.process():
            print(f"Received message: {message.body.decode()}")
            # Process the message here (e.g., handle a front-end action)
            
    async def listen_for_messages(self, queue_name):
        connection = await aio_pika.connect_robust(self.amqp_url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True)
            await queue.consume(self.on_message)

    def start_consuming(self, queue_name):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen_for_messages(queue_name))

    async def subscribe(self, queue_name: str, callback: Callable):
        connection = await aio_pika.connect_robust(self.amqp_url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True)

            async def on_message(message):
                async with message.process():
                    message_body = json.loads(message.body.decode())
                    if self.filter_messages(message_body, {"type": "back-end"}):  # Example filter
                        await callback(message_body)
                    else:
                        print(f"Message filtered: {message_body}")

            await queue.consume(on_message)

    async def filter_messages(self, message: dict, criteria: dict) -> bool:
        # Implement simple message filtering (can be customized)
        return all(item in message.items() for item in criteria.items())

    async def send_to_websockets(self, message: dict):
        # Send message to all connected WebSocket clients
        for client in self.websocket_clients:
            await client.send_json(message)
            print(f"Sent to WebSocket: {message}")
