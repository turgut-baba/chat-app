# InterviewLIB Documentation

Welcome to the official documentation for InterviewMQ, a Python asynchronous message queue for handling multiple client requests. This document has details about how to run and use it.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Endpoints](#getting-started)
4. [Examples](#examples)

---

## Introduction

**InterviewMQ** is a message queue designed to handle multiple messages at the same time. It runs on it's own port and handles consumers (subscribers) and publishers. Ideally there should be 3 services running for a minimal example: InterviewMQ service, consumer service and a publisher service. The consumer and InterviewMQ should have an open connection to work. The publishers only send a trigger to broadcast messages.

2 main endpoints are:

- restful: Handles http requests without the command keyword for consumers and producers.
- websocket (reccomended): Handles websocket connections for consumers and producers.

---

## Installation

For installation refer to README.md on [GitHub](https://github.com/turgut-baba/chat-app/blob/main/README.md) 

### Requirements

- Python 3.6+
- Dependencies (automatically installed):
  - websockets
  - json
  - asyncio
  - uvicorn
  - httpx
  - fastapi

---

## Endpoints

### websocket

There is a single function to connect to websocket and one url: /interviewmq. To connect to a websocket endpoint you need to send a json with at least 2 tags: topic and command. The command is what you want to do that being subscribe or publish. 

If you want to publish a message you also need to provide a message. The tag for message is **msg** , if you write message as a tag it won't work.

Your payload should look like this:
For publishing:
```json
payload = {
    'msg': 'Test message here.',
    'topic': 'test_topic',
    'command': 'publish'
}
```

For subscribing:
```json
payload = {
    'topic': 'test_topic',
    'command': 'subscribe'
}
```

To connect to the websocket endpoint, you need to connect to this url:

```
ws://localhost/interviewmq
```

For subscribing a connection must remain oppen so it's suggested to use an asyncron library like asyncio or fastapi.

### http

Http protocol uses 2 endpoints, subscribe and publish. There are two url's to connect each individual endpoint:

```
http://localhost/interviewmq/subscribe
```

```
http://localhost/interviewmq/publish
```

Since the command mechanism works internally here, only topic and message is sufficient on this endpoint.

Again for consumers an open async. client connection stream needs to be established to work.

The payload is similar to websocket without the command tag:
For publishing:
```json
payload = {
    'msg': 'Test message here.',
    'topic': 'test_topic'
}
```

For subscribing:
```json
payload = {
    'topic': 'test_topic'
}
```



Once everything is set, while the subscribers are listening every message published to the queue will be sent to each subscriber.