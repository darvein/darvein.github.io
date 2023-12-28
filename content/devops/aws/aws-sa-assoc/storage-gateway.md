# AWS Storage Gateway

An AWS service that allows on-premise network to direct connect with AWS (via AWS Direct Connect) and store data on different services, s3 or glacier.

## Generalities
- It is runs a VM that can run on a VMWare/Hypervisor
- Provides local storage backed by S3/Glacier
- Used by DR environments
- Used by Cloud Migrations

## Types
- NFS (File Gateway)
    - Can be stored on S3 via NFS/SMB
    - Ownership, permissions and timestamps are preserved in s3 obj meta-data
    - Supports native objects functionality (lifecycle, cross-region replication, etc)
- iSCSI (volumes gateway, non flat, block-based storage): for Operating Systems, DB engines.
    - It is stored in AWS EBS
    - Backups are incremental, only changed blocks are captured
    - Stored volumes: This are backed up to S3 from on-prem to S3 as multi-part uploads (1Gb-16TB). No AWS EBS.
    - Cached volumes: Data is captured from on-premises to EBS and finally to S3 (1Gb-32TB).
- VTL (tape gateway): archiving and/or backup solution.

## Modes
- File gateway
  - Stored in S3 via NFS or SMB
- Volume Gateway Stored Mode (Gateway-stored volumes)
  - iSCSI storage
  - Async replication from on-prem data to S3
- Volume Gateway Cached Mode
  - iSCSIS storage
  - Cached in AWS S3
- Tape Gateway
  - iSCSI interface
  - Tabe Library with exsting backup software (VTL)
