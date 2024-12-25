from api.MessageQueue import MessageQueue
from system.message import Message
from typing import Callable

class Queue(MessageQueue):
    def __init__(self, port: str):
        self.port = port
        self.messages = []

    def queue_message(self, Process: Callable) -> bool:
        message = Message("")
        message.set_in_quee(True)

        message.add_process(Process)

        self.messages.append(message)


    def send_queued_messages(self):
        for message in self.messages:
            connection = await aio_pika.connect_robust(self.connection_url)
            async with connection:
                channel = await connection.channel()
                await channel.default_exchange.publish(
                    aio_pika.Message(body=str(message).encode()),
                    routing_key=topic
                )
