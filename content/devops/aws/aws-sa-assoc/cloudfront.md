# Cloudfront

It is a content delivery service. Content is replicated across different edge location. An edge location is not a region nor a AZ, it is a location where data is cached.

- it caches static content (web distribution), dynamic, streaming (rtmp) data.
- it well integrates with s3, ec2, elb, route53.
- a origin for the CDN can be a ec2, s3 or a elb.
- objs in CDN are cached with a TTL
- manually cleared objs are charged by aws.

- it supports integration with AWS WAF
- it supports geo restrictions accesses
