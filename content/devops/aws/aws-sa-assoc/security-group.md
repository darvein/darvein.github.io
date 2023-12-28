# Segurity groups

A virtual firewall.

## Basics

- Controls inbound and outbound traffic
- Inbound is blocked by default
- Outbound is allowed by default
- EC2: mutliple SGs can be assigned
- SGs are STATEFUL (ACLs are stateless)

## Best practices

- Don't block specific ip address with SGs instead use NACLs
