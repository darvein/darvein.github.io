# VPN

### Site-to-site VPN

- Connects a VPC with on-prem subnets
- VGW -> CGW, has HA by default
- Works for 1.25 Gbps
- Costs per each Gb out/in
- Considered as backup of Direct Connect, means, not stable

### Accelerated site to site

- 2 IPSec
- Global accleration underneath
- Can be used only if TWG is used

### BGP

- AS / ASN
- It is a routing protocol
- BGP vs eBGP

### Global Accelerator

- Anycast ip addresses
- Less routers hops to reach AWS Network
- Works with TCP and UDP
- At Network Level (OSI)
