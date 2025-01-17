from fastapi import HTTPException, Request
from InterviewMQ.Queue import connected_clients, topics, router
from InterviewMQ.system.message import Message
import asyncio
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse

@router.post("/interviewmq/subscribe")
async def subscribe(message: Message, request: Request):
    """
    Subscribe to the message queue using Server-Sent Events (SSE).
    """
    topic = message.topic

    queue = asyncio.Queue()
    await connected_clients.add_sse_connection(topic, queue)
    
    async def event_stream():
        try:
            while True:
                message = await queue.get()
                yield f"data: {message}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            await connected_clients.remove_sse_connection(topic, queue)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@router.post("/interviewmq/publish")
async def publish(message: Message, request: Request):
    """
    Publish a message to all connected subscribers.
    """
    topic = message.topic
    msg = message.msg
    
    if not msg or not topic:
        raise HTTPException(status_code=400, detail="Message content is required")

    await connected_clients.broadcast(topic, msg)

    return JSONResponse(content={"status": "Message sent to subscribers"}, status_code=200)



