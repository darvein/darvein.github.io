# VPC

- In order to connect a VPC with on-prem: Direct Connect or VPC
- VPC supports dhcp service
- VPC supports DNS
- NTP support

### Route tables

- High CIDRS masks have high priority

### Stateless

- Need to specify ports in and out

### Stateful

- Automatically knows what port to use as return

### NACL

- 1 per subnet
- Stateless
- it is based on rules
- 1 acl can be used in multiple subnets

### SGs

- Allows only, it doesn't deny
- A SG can be referenced to another SG
- A SG can be self-referenced
