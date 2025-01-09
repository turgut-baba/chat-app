from InterviewLIB.src import ConsumerImpl 
import asyncio

client = ConsumerImpl("ws://localhost:8000/interviewmq")
asyncio.run(client.subscribe("foo"))

client.start_listening()
