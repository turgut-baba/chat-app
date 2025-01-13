# InterviewLIB Documentation

Welcome to the official documentation for InterviewLIB, a Python library for abstracting producer and consumer mechanisms that communicate with InterviewMQ. This document has details about each function.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Functions](#getting-started)

---

## Introduction

**InterviewLIB** is a Python library designed to provide a simple interface to write microservices that communicate with InterviewMQ. It aims to provide simplicity and ease of use in a normally bloated microservice code.

2 main classes:

- Producer: Sends a message on a topic to a message queue. 
- Consumer: Subscribes to a topic and allows filters to messages.

---

## Installation

For installation refer to README.md on [GitHub](https://github.com/turgut-baba/chat-app/blob/main/README.md) 

### Requirements

- Python 3.6+
- Dependencies (automatically installed):
  - [Dependency 1]
  - [Dependency 2]

---

## Methods

### Producer

**publish**

Signature:
    ```python
    async def publish(self, message, topic)  
    ```

brief: 
    Sends a message on a given uri asynchronously. Uses websockets to connect. 
    This function is the main part of a Producer microservice. Communicates with json.

parameters:
    - self -> instance 
    - message -> The message to be sent to the message queue which a subscriber will recieve if they are subscribed to the same topic. Please note that the consumer can filter a message and not recieve it if the sent message does not fit the criterias.
    - topic -> The topic in which the message will go to. For a consumer to recieve the message they must subscribe to the same topic as this.

### Consumer

**subscribe**

Signature:
    ```python
    def subscribe(self, topic)  
    ```

brief: 
    Sends a message on a given uri asynchronously. Uses websockets to connect. 
    This function is the main part of a Producer microservice. Communicates with json.

parameters:
    - self -> instance 
    - message -> The message to be sent to the message queue which a subscriber will recieve if they are subscribed to the same topic. Please note that the consumer can filter a message and not recieve it if the sent message does not fit the criterias.
    - topic -> The topic in which the message will go to. For a consumer to recieve the message they must subscribe to the same topic as this.
    
**start_listening**

    