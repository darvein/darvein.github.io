# EC2

## Basics

- EC2 instances backed with EBS can easily recovered by restarting into a  different hypervisor InstanceStore in the other hand if the instance fails, the machine and data is lost.
- Supports user data if a script execution is needed after the machine is boot.
- ** clustered placement group (one AZ) and spread placement group (multiple AZs).
- Nitro and XEN are the underlying hypervisors for AWS EC2

### Options

- on-demand: hourly paid.
- reserved: 
     - predicatable usage. 
     - Up-front payments with a contract (Standard, Convertible, Scheduled RIs)
     - from 1 to 3 years terms. The most time the most cheaper
     - cannot be moved between regions
- spot: 
    - low prices
    - flexible start and end times by biding a price
    - if the instance is terminated by aws the partial hour of usage is not charged, if you terminate the instance yourself you will be charged for the complete hour
- dedicated: regulary stuff, no multitenant virt. Paid in hourly basis and also as a ReservedInstance

### Types of EC2

- field programmable gate array (F1): financial, big data
- high speed storage (I3): nosql dbs, data warehousing
- graphics intensive (G3): video encoding, 3d streaming
- high disk throughput (H1): mapreduce-based workloads, HDFS or MAPR-FS
- lowest cost, general purpose (T2): web servers
- dense storage (D2): fileservers, hadoop
- memory optimized (R4, X1): mem intensive. SAP HANA
- general purpose (M5): app services
- compute optimized (C5): cpu intensive
- graphics general purpose GPU (P3): ML, Bitcoin mining


### Checks

- system status checks: Hypervisor issues
- instance status checks: OS issues or config, network issues

## IAM roles into EC2 instances

- An IAM role can be attached to a EC2 on the fly.
- AWS Creds are injected in the instance and automatically rotated
- For the `awscli` it is needed to specify the `--region $REGION` when accessing to a different bucket region from the origin.


## AWS EC2 Metadata

- `http://169.254.169.254/latest/meta-data`
    - `/public-ipv4`
- `http://169.254.169.254/latest/user-data`

## Autoscaling groups

- Requires a load balancer in place
- Requires a lunch configuration: Like when we create a EC2 (ami, network, vpc, sg, etc).
- Provides redundancy on multiple AZs (multiple subnets).
- Autoscale policies setup based on Alarms tresholds. Increase and Decrease rules.
- Notifications on autoscaling group attaches or removes instances.
