# Virtual hard disk. Block based storage.

## Generalities
- Tied to a single AZ
- Can be attached to only one EC2 instance at once
- EBS has to be in the AZ (subnet) than the EC2. 
    - Otherwise move the EBS to other AZ by creating a Snapshot. Same for regions.
- Can be modified/upgraded on the fly
- Multiple EBS mounted in a EC2 can help to form a RAID 5/10/0

## Defaults
- Termination protection is turned off by default
- EBS root vol is by default deleted once upon EC2 termination

## Encryption
- EBS root volume CAN NOW be encrypted (only via thrid party solutions). non-root volumes can be encrypted.

## Types
- General purpose SSD (GP2): SSD
    - ratio of 3iops per GB up to 10000iops
    - ability to burst up to 3000iops for extended periods of time on 3334Gb volumes and above
- Provisioned IOPS SSD (IO1): SSD
    - high performance apps
    - NOSql databases
    - more than 10000iops
    - low latency
- Throughput optimized HDD (ST1): Magnetic
    - low cost for frequently access
    - big data, data warehouses
    - cannot be a boot volume
    - log processing
- Cold HDD (SC1): Magnetic
    - low cost for less frequently access
    - low cost
- Magnetic: Magnetic
    - lowest cost per Gb
    - legacy option!
    - data access infrequently
    - can be a boot volume

## Snapshots
- Stored in S3
- Snapshots are incremental copies
- AMIs can be created from a EBS
- Shareable snapshots cannot be encrypted
- Snapshots can be migrated to new AZ or Region
- Snapshots are cost effective
- Service AWS Data Lifecycle Manager to automate snapshots + retention rules

## Charges / Pricing
- SDD ebs are more expensive than HDD ebs
