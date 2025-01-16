from InterviewLIB.api import Consumer, ConnectionMethod
import asyncio
from fastapi import FastAPI

app = FastAPI()

client = Consumer("http://localhost:8000/interviewmq")
client.set_filter("Hello")
client.set_connection(ConnectionMethod.HTTP)
asyncio.run(client.subscribe("foo") )


if __name__ == "__main__":
    import uvicorn
    #uvicorn.run(app, host="localhost", port=8080)
