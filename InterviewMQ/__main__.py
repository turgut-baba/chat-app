import sys
from fastapi import FastAPI

if __name__ == "__main__":
    import uvicorn

    service_port = 8000

    if len(sys.argv) > 1:
        try:
            service_port = int(sys.argv[1])
            if service_port > 9999 or service_port < 1000:
                raise ValueError
        except ValueError:
            print("Please enter a valid integer between 1000-9999. Or leave it blank for default 8000")
            quit()

    uvicorn.run("InterviewMQ:app", host="0.0.0.0", port=service_port, reload=True)