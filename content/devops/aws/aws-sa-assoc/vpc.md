# VPC

## Basics

- supports hardware virtual private network VPN for on-prems datacenters
- limit of 5 VPCs by default
- components: 
    - igw or vpg (vpn)
    - routing tables
    - nACLs
    - subnets
    - vpc
    - region
- 1 subnet = 1 AZ
- LAN options:
    - 10.0.0.0 - 10.255.255.255  (10/8)
    - 172.16.0.0 - 172.31.255.255 (172.16/12)
    - 192.168.0.0 - 192.168.255.255 (192.168/16)
- Only 1 IGW per VPC
- ** SGs are stateful. NACLs are stateless.
- instead of a igw a NAT Instance (ec2) can be used or just a Nat gateway (EIP)
- network traffic logs can go to cloudwatch via VPC FLowLogs option enabled (not peered vpcs)
- vpc flow can be created at VPC, subnet and network intf levesl
- VPC endpoints can be enabled to allow internal aws ec2 instances to connect to other aws services (s3)
- vulnerability scans are not allowed, even on your own VPC
- when creating a vpc it by defaults create: ACL, SGs and a RT
- Egress-Only, allows vpc based ipv6 access to the internet, but prevents outisde ipv6 connections to the vpc


## Subneting

- on a VPC, the first 4 IP addrs and the latest one are reserved for AWS
    - .0 network addr
    - .1 aws vpc router
    - .2 aws dns server
    - .3 aws for the future
    - .255 network broadcast
- At least two subnets should be public (multi AZs)

## VPC Peering

- connect a vpc with another via a direct network route using private IP addrs
- VPCs can be from different aws accounts
- VPCs are not transitives only 1-1

## NAT Gateways

- IGW allows in and out access to internet to the public subnets and the resources on it
- NAT gateway (and NAT instance) allows resources from a subnet access to internet but no the other way around
- SGs cannot be associated with a NAT gateway
- A Nat gateway operates only in one AZ, it is needed one on each AZ
- scales up automatically to 10Gbps
- automatic ip addr assignment

### Bastion host

- it has to be in the public subnet ?


## NALCs

- inbound and outbound rules definition
- by default deny anything and deny everythingA
- ephemeral ports 32768-65535. There may be some differences on LBs and Windows Server.
- rules are numered on 100 range steps for the ALLOW rules. The inner options would be for DENY rules.

## VPN

- requires at least a VPG and a Customer gateway
