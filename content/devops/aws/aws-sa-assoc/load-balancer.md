# Load Balancer

## Basics

- Types: Application, Network, Classic load balancer.
- X-forward-For header is forwared from outside to the instance server
- HTTP 504 if the backend app is having issues, not reacheable.
- LBs costs money :)

## Application load balancer

- HTTP/HTTPS (based on methods, routes)
- operates on layer 7

## Network load balancer

- TCP traffic based
- layer 4
- millions of requests per second, ultra low latencies

## Classic load balancer

- Elastic load balancer
- Mix of layer 7 and 4.
- Mix of HTTP/HTTPS and other TCP specifics
