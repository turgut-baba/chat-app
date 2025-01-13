from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from fastapi.staticfiles import StaticFiles
from InterviewLIB.api.Producer import Producer

app = FastAPI()

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
    producer = Producer("ws://localhost:8000/interviewmq")
    response = await producer.publish("foo", "Hello Stryker!")
    return {"message": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)

