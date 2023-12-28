# Lambda

## Basics

Serverless service. The underlying infrastructure is managed by AWS.

- Even-driven compute service (s3, dynamodb)
- Response of HTTP requests via AWS API Gateway
- Supports multiple languages engines (node, python, c#, java).
- An IAM Role is needed
- A variaty of triggers (alexa skills, cloudfront, cloudwatch, dynamodb, s3, , api gateway, etc).
- 1 lambda function execution per request.

The evolution would be Data Centre -> IaaS -> PaaS -> Containers -> Serverless.

What languages support?: nodejs, java, python, c#, go, powershell and also docker!

### Pricing

- f<<irst 1 millons request are free. $0.20 per 1 million requests afterwise.
- priced per time execution rounded to 100ms.
- priced on the amount of mem allocated for the function execution, $0.00001667 for evert Gb/sec used.
