from InterviewLIB.src import ConsumerImpl 
import asyncio
import websockets
import json

client = ConsumerImpl("ws://localhost:8000/interviewmq")
asyncio.run(client.subscribe("foo"))

client.start_listening()
