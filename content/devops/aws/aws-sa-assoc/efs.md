# EFS Elastic filesystem

- Can be attached to multiple ec2 instances at once
- Scales automatically on size of storage
- Supports NFSv4
- Works only within a Region and multiple AZs in the Region
- Multi-AZ replication
- Read after write consistency
- Can be mounted from on-premises (unsecure without tunnels)
  - Or se AWS Datasync in on-prem infra to sync data to EFS
- Preserves ownership and permissions from OS
- You pay for what the size you currently use
- Multiple EFS' can be in sync with with AWS DataSync

## Pricing
- 3x times more expensive than EBS
- 20x times more expensive than S3
