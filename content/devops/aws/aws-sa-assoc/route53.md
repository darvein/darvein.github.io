# Route53

- Global AWS service
- Supports public and private Hosted zones
- Initial limit of 50 domain registration only


## Routing policies

it basically supports:

- simple routing
    - Records that routes to something: MX, A, CNAME, TXT, etc.
- weighted routing
    - basically splits traffic between targets based on a weight number (0-100)
- latency-based routing
    - route53 automatically routes based on the origin's response latency (ec2 or lb)
- failover routing
    - a route53 healthcheck setup is needed
    - works for DR environments
    - two record sets is nedded, one primary and the other secundary
- geolocation routing
    - based on the client's region geolocation
    - region locations has has to manually be configured in route53
- geoproximity
    - based on the geolocation of the aws resources
- multivalue answer routing
    - basically multivalue servers to server a specific A dns record
