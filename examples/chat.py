from src.api.MessageQueue import MessageQueue

chat_queue = MessageQueue()

def my_message():
    return "Hi"

chat_queue.queue_message(my_message)

chat_queue.send_queued_messages()