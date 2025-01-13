from InterviewLIB.api import Consumer, ConnectionMethod
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

client = Consumer("ws://localhost:8000/interviewmq")
client.set_filter("Hello")
asyncio.run(client.subscribe("foo") )



if __name__ == "__main__":
    import uvicorn
    #uvicorn.run(app, host="localhost", port=8080)
