# AWS Kinesis

Service for high support streaming data from different sources (games, amazon purchaces, stock pirces, etc)

## Basics

- 3 kinesis: Streams, Firehose and Analytics
- producers (ec2, mobiles, computers, IoT devs)
- consumers (ec2 instances, redshift, elasticsearch)

## Kinesis Streams

- data producers -> kinesis streams (stored 24h-7days) in shards -> data consumers -> storage
- the capacity is measured by the number of shards

## Kinesis Firehose

- data producers -> kinesis firehose (not need for data consumers nor shards) -> s3 -> data consumers
- data is not stored, it gets deleted as soon is proceesed by firehose

## Kinesis Analytics

- data procucers -> kinesis analytics -> data consumers (s3, redshift, es)
- fast sql over the data
