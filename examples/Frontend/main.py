from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from fastapi.staticfiles import StaticFiles
from InterviewLIB.api import Producer, ConnectionMethod
import sys

app = FastAPI()

PORT = 8080
MQ_PORT = 8000
if len(sys.argv) > 2:
    try:
        MQ_PORT = int(sys.argv[2])
        if MQ_PORT > 9999 or MQ_PORT < 1000:
            raise ValueError
    except ValueError:
        print("Invalid value for message queue port. (first argument)")
        MQ_PORT = 8000


app.mount("/static", StaticFiles(directory=os.path.dirname(__file__) + "/static/"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    file_path = os.path.join(os.path.dirname(__file__), "static/index.html")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>404 Not Found</h1>", status_code=404)

@app.get("/send_backend")
async def test_endpoint():
    producer = Producer("ws://localhost:" + MQ_PORT + "/interviewmq")
    producer.set_connection(ConnectionMethod.WS)
    response = await producer.publish("foo", "Hello Stryker!")
    return {"message": response}

if __name__ == "__main__":
    import uvicorn
    import sys

    service_port = 8080


    try:
        service_port = int(sys.argv[1])
        if service_port > 9999 or service_port < 1000:
            raise ValueError
    except ValueError:
        print("Service port is faulty, opting in for the default one 8080.")
        service_port = 8080
    except IndexError:
        service_port = 8080
        
    uvicorn.run(app, host="localhost", port=service_port)

