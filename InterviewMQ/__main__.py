import sys
from fastapi import FastAPI

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("InterviewMQ:app", host="0.0.0.0", port=8000, reload=True)