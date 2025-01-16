from InterviewLIB.api import Consumer, ConnectionMethod
import asyncio
from fastapi import FastAPI
import sys

MQ_PORT = 8000

if __name__ == "__main__": 

    if len(sys.argv) > 1:
        try:
            MQ_PORT = int(sys.argv[1])
            if MQ_PORT > 9999 or MQ_PORT < 1000:
                raise ValueError
        except ValueError:
            print("Please enter a valid integer between 1000-9999. Or leave it blank for default 8000")
            quit()

    client = Consumer("ws://localhost:" + str(MQ_PORT) + "/interviewmq")
    asyncio.run(client.subscribe("foo") )
