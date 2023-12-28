# SQS

First service ever on AWS.
Distributeded queue system for messages between applications

## Basics

- it is a PULL based system
- messages can contain up to 256 Kb of text on any format
- messages can be retrieved via AWS SQS API
- messages can be kept in queue from 1min to 14 days (default is 4days)
- autoscaling can be built into the service
- SQS guaratees that messages will be processed at leas once
- Supports dead-letter queue for not consumed? messages
- FIFO queue is optional (limits?)
- Only works over HTTP

### SQS visibility (when consumers are consuming the message)

- a message becomes invisible if there is an external job reading the message, the message becomes invisible. If for some reason the external job takes too much time and exceeds the SQS timeout then the message becomes visible again and another job/reader can take the message and delivery it (possible twice delivery).
- default visibility timeout is 30sec
- maximum is 12 hrs

### Long polling

- Long polls from the EC2 instance to the SQS with a timeout
- Long polls are cheaper
- Long polling, polls the queue periodically and only returns a response if there is a message in the queue or timeout is reached
- Short polling returns inmediately even if no messages are in the queue

## Queues

### Standard queues

- default one
- messages copies can be delivered out of order on a high messaging traffic scenario
- unlimimted number of transactions per second
- best ordering
- messages have to be explicitely deleted from the queue

### FIFO queues

- messages are delivered exactly in the same order, no matter what
- 300 transacations per second (TSP)

## Resources

- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dg.pdf
