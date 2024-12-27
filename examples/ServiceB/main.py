from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import pika
import json
import threading

app = FastAPI()

# Store WebSocket connections
connected_clients = set()

# RabbitMQ Consumer Logic
def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue')

    def callback(ch, method, properties, body):
        task = json.loads(body.decode('utf-8'))
        print(f"Processing Task: {task}")
        for client in connected_clients:
            try:
                # Send message to connected WebSocket clients
                import asyncio
                asyncio.run(client.send_json({"task": task}))
            except Exception as e:
                print(f"Failed to send message: {e}")

    channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=True)
    print("Started consuming tasks...")
    channel.start_consuming()

# Start RabbitMQ Consumer in a background thread
thread = threading.Thread(target=consume_messages, daemon=True)
thread.start()

# WebSocket Endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print("New WebSocket client connected")
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("WebSocket client disconnected")