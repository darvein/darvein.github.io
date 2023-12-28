# SNS Simple notification service

## basics

- powerful notification system
- push-based service
- publish-subscribe (pub-sub) messaging paradigm. No periodically checks.
- integrations with aws autoscaling, email notif, SMS, HTTP Endpoints, etc.
- messages are stored reduntantly across different AZs 
- message format for email is JSON
- Only works over HTTP

## topics

- where subscribers are grouped in order to get an identical copy of the message notification
- a single topic can support multiple endpoints for delivery such as iOS, android, SMS recipients, etc.

## pricing

- cheaper, basically you pay as you go model. No upfront costs.
- $0.50 per 1 million SNS requests
- $0.06 per 100,000 deliveries over HTTP
- $0.75 per 100 deliveries over SMS
- $2 per 100,000 deliveries over email

## Resources

- https://docs.aws.amazon.com/sns/latest/dg/sns-dg.pdf
