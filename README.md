# Getting Started with InterviewMQ and InterviewLIB

Welcome to InterviewMQ/LIB, a Python library and server with two parts:
An optional abstraction library caleld InterviewLIB that help write consumer and producer microservices and a message queue server called InterviewMQ. This guide will help you get started quickly and effectively.

---

## Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Features Overview](#features-overview)
4. [Examples](#examples)
5. [Further Reading](#further-reading)

---

## Installation

To install InterviewMQ, you can directly use it's source code or use pip like so:

```bash
pip install -e .
```

Make sure your environment has Python 3.6 or higher.

### Verify Installation
Run the following command to verify that the library was installed correctly:

```bash
python -c "import InterviewLIB; print('InterviewLIB installed successfully!')"
```

---

## Basic Usage

For running the examples with minimal effort, simply run setup_and_run.py like so:
```bash
python setup_and_run.py
```

Simply follow the instructions after running and this will run the InterviewMQ server 
and run the publisher and consumer clients inside examples.

### InterviewMQ

Here is how to run InterviewMQ:

```bash
python -m InterviewMQ
```

This will run on a localhost on port 8000.

or 

```bash
uvicorn InterviewMQ.Queue:app --host 0.0.0.0 --port 8000 --reload
```

### InterviewLIB

Here is a simple example to get started with InterviewLIB.

Please note that InterviewMQ server should be up and running for this to work.

After running the server a consumer server must subscribe to the message queue with a 
certain topic. To do this the InterviewLIB has a neat abstraction called the Consumer class.

```python
from InterviewLIB.src import ConsumerImpl 
import asyncio

client = ConsumerImpl("ws://localhost:8000/interviewmq")
asyncio.run(client.subscribe("foo"))

client.start_listening()
```

Ofcourse you can manually connect to the message queue with the port and the uri manually.
If you do so, the json you send must look like this:

```json
subscription = {
            "command": "subscribe",
            "topic": "your_topic"
        }
```

Similarly there is an interface for publisher class too Here is what an app looks like with the Publisher class:

```python
from InterviewLIB.src import ProducerImpl

client = ProducerImpl("ws://localhost:8000/interviewmq")
client.publish("foo", "Test message is sent!")
```

And for the manual connection for a publisher the json should look like this:
```json
message = {
        "command": "publish",
        "topic": "your_topic",
        "msg": "your_message"
    }
```

For detailed API documentation, refer to the [official documentation](#further-reading).

---

## Features Overview

InterviewMQ provides the following key features:

- **Publish:** Publish a message to the message queue so every microservice subscribed to that message can recieve that message asyncronously.
- **Subscribe:** Subscribe to the server on a given topic so that if or when a publisher publishes a message in that topic recieve the message.
- **Message filtering:** For a given consumers add a filter to the messages so that only the filtered messages can be seen.
- **Retry:** If a message fails to go through the server will retry a set amount of times. You cen set the amount of retries.

These features enable you to have a communication mechanism that allows different parts of a system to exchange information without needing to wait for each other to process the messages immediately.

---

For more examples, check the [examples directory](https://github.com/turgut-baba/chat-app).

---

## Further Reading

- **API Reference:** [API Documentation](https://your-library-docs.com)
- **Source Code:** [GitHub Repository](https://github.com/your-repo)
- **Community Support:** [Discussion Forum](https://community.your-library.com)

For additional assistance, feel free to contact me at [turgutbababalim@gmail.com](mailto:urgutbababalim@gmail.com).

---

Thank you for using Interview! I thank everyone at Stryker who had the time to read this documentation, I hope you liked this repository and I'm eager to hear back from you!

