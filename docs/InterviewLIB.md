# InterviewLIB Documentation

Welcome to the official documentation for InterviewLIB, a Python library for abstracting producer and consumer mechanisms that communicate with InterviewMQ. This document has details about each function.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Functions](#getting-started)
4. [Examples](#examples)

---

## Introduction

**InterviewLIB** is a Python library designed to provide a simple interface to write microservices that communicate with InterviewMQ. It aims to provide simplicity and ease of use in a normally bloated microservice code. It provides basic functionality like message filtering, retries, and http/ws connections.

2 main classes are:

- Producer: Sends a message on a topic to a message queue. 
- Consumer: Subscribes to a topic and allows filters to messages.

---

## Installation

For installation refer to README.md on [GitHub](https://github.com/turgut-baba/chat-app/blob/main/README.md) 

### Requirements

- Python 3.6+
- Dependencies (automatically installed):
  - websockets
  - json
  - httpx
  - fastapi

---

## Methods

### Producer

#### publish

Signature:
    ```python
    async def publish(self, topic, message)  
    ```

brief: 
    Sends a message on a given uri asynchronously. This function is the main part of a Producer microservice. Communicates with json.

    The default connection method is with ws, which a ws url is expected. If you want to use http instead, you can set the connection type before calling this function using [set_connection](##set_connection)

parameters:
    - self -> Instance.

    - topic -> The topic in which the message will go to. For a consumer to recieve the message they must subscribe to the same topic as this.

    - message -> The message to be sent to the message queue which a subscriber will recieve if they are subscribed to the same topic. Please note that the consumer can filter a message and not recieve it if the sent message does not fit the criterias.

#### set_filter

Signature:
    ```python
    def set_filter(self, filter: Union[str, Callable])
    ```

brief: 
    Set a filter as a string or a callable. If you set a string it will only return 
    results that contains the given string. If you provide a callable it will add the 
    message as a paramter to the callable and returns a bool that will decide whether to return the message or not.

parameters:
    - self -> Instance.

    - filter -> The filter, can be either string or a callable. The string should be the substring that will be searched in the published string. The callable should take a string as an argument and return a boolean.

#### set_retries

Signature:
    ```python
    def set_retries(self, retries: int)
    ```

brief: 
    Set how much a publish should be retried for. Default is 3.

parameters:
    - self -> Instance.

    - retries -> he amount of retries.

#### set_connection

Signature:
    ```python
    def set_connection(self, Connection: ConnectionMethod)
    ```

brief: 
    Set how the [publish](####publish) method would work. The two options are http or websocket.

parameters:
    - self -> Instance.

    - Connection -> ConnectionMethod enum that has either http or ws.

### Consumer

#### subscribe

Signature:
    ```python
    async def subscribe(self, topic)
    ```

brief: 
    Sends a message and starts listening on a given uri asynchronously. This function is the main part of a Consumer microservice. Communicates with json. Since it starts listening and keeps running, it's reccomended to use with asyncio.run().

    The default connection method is with ws, which a ws url is expected. If you want to use http instead, you can set the connection type before calling this function using [set_connection](####set_connection)

parameters:
    - self -> Instance.

    - topic -> The topic to start listening to. Every message that is not filtered will be recieved in that topic.

#### set_filter

Signature:
    ```python
    def set_filter(self, filter: Union[str, Callable])
    ```

brief: 
    Set a filter as a string or a callable. If you set a string it will only return 
    results that contains the given string. If you provide a callable it will add the 
    message as a paramter to the callable and returns a bool that will decide whether to return the message or not.

parameters:
    - self -> Instance.

    - filter -> The filter, can be either string or a callable. The string should be the substring that will be searched in the recieved string. The callable should take a string as an argument and return a boolean.

#### set_retries

Signature:
    ```python
    def set_retries(self, retries: int)
    ```

brief: 
    Set how much a publish should be retried for. Default is 3.

parameters:
    - self -> Instance.

    - retries -> he amount of retries.

#### set_connection

Signature:
    ```python
    def set_connection(self, Connection: ConnectionMethod)
    ```

brief: 
    Set how the [subscribe](####subscribe) method would work. The two options are http or websocket.

parameters:
    - self -> Instance.

    - Connection -> ConnectionMethod enum that has either http or ws.


# Examples

## Publisher example

```
producer = Producer("ws://localhost:8000/interviewmq")

producer.set_filter("Hello")

# or ConnectionMethod.HTTP, but dont forget to change the url.
client.set_connection(ConnectionMethod.WS)


response = await producer.publish("example_topic", "Hello World!")
```


## Consumer example

```
client = Consumer("http://localhost:8000/interviewmq/subscribe")

client.set_filter("Hello")

# or ConnectionMethod.WS, but dont forget to change the url.
client.set_connection(ConnectionMethod.HTTP)

asyncio.run(client.subscribe("example_topic") )
```