""" from fastapi import FastAPI
import pika
import json

app = FastAPI()

# RabbitMQ Connection
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue')
    return channel, connection

@app.post("/publish/{task_id}")
async def publish_message(task_id: int):

    task = {"task_id": task_id, "task_name": f"Task-{task_id}"}
    
    channel, connection = get_rabbitmq_channel()
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(task)
    )
    connection.close()
    return {"message": f"Task {task_id} published to queue"}
 """

import asyncio
import websockets
import json

from InterviewLIB.src import ProducerImpl

client = ProducerImpl("ws://localhost:8000/interviewmq")
client.publish("foo", "Hello stryker team, this is my application!")

