from InterviewLIB.src import ProducerImpl

client = ProducerImpl("ws://localhost:8000/interviewmq")
client.publish("foo", "Hello stryker team, this is my application!")

