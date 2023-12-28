# DynamoDB

## Basics

- Fast nosql: mobile, web, gaming, ad-tech, IoT, etc.
- Low latency to applications.
- Expensive for writes, cheaper for reads.
- Stored on SSD
- Spread across 3 geographicall distinct data centres (AZs)
- dynamodb read/write capacity scales on the fly, no downtimes

- eventual consisten reads
    - consistency acorss all copies of data is within a second (best read performance)
- strongly consisten reads
    - returns the results that reflects all writes were successful, prior the read

## Indexes

- ?

## Pricing

- based throughput capacity (write/read)
    - read capacity units billed un blocks of 50 per unit
    - write capacity units billed un blocks of 10 per unit
