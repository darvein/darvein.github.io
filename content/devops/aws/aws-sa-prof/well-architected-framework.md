# Well architected framework


## The framework

Collection of best practices and architectural definitions to provide a well designed cloud infrastructure based on the 5 pillars: operational excellence, security, reliability, performance efficiency and cost optimization.

### Generalities

#### design principles

- stop guessing your capacity needs
- test systems at prod scale
- automate to make architectural experimentatino easier
- allow for evolutionary architectures
- data-driven architecures
- improve through game days

## (I) Operational excellence

## (II) Security

### Design principles

- Apply security at all layers (acls, sgs, ec2)
- Enable traceability (cloudtrail)
- Automate response to security events (SNS, brute-forces)
- focus on securing your system
- automate security best practices (hardened amis)

### Definitions

#### data protection

Data should be segmented and classified so certain data can be only accesible by certain group of persons and no others.
**AWS Key services:** elb, ebs, s3, rds (encryption)

#### privilege management

Only specific, authorized and authenticated users should access to the right resources. This can be defined by ACLs, Rol Based access, Secure passwords. The root account has to be protected. IAM roles and groups has to be well defined and verified.
**AWS Key services:** iam, mfa

#### infrastructure protection

Better to check enforncement level, host or network. Protection and integrity checks on the EC2 machines.
**AWS Key services:** vpc, nat instances, sgs, nacls, public/private subnets.

#### detective controls

Measures to detect security breachs. Proper logging agregation in place.
**AWS Key services:** cloudtrail, cloudwatch

## (III) Reliability

### Design principles

- test recovery procedures
- automatically recover from failures
- scale horizontally to icnresae aggregate system availability
- stop guessing capacity, don't over provision.

### Definitions

#### foundations

This is fully managed by AWS as part of the infrastructure physical provisioning of resources. AWS defines some limitations so users don't over provision resources, those limits are not fixed, they can be increased by creating tickets.
AWS Key services: iam, vpc

AWS Limits: https://docs.aws.amazon.com/general/latest/gr/aws-service-information.html

#### change management

A tracking system or versioning needs to be in place as well as monitoring.
AWS Key services: cloudtrail

#### failure management

Always assume that a failure will occure, so how to recover?
AWS Key services: cloudformation

## (IV) Performance Efficiency

## (V) Cost Optimization

## References

- Source: https://aws.amazon.com/architecture/well-architected
