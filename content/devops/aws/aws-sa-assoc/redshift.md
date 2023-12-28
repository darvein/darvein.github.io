# Redshift

OLAP data housing service.
Data is organized in columns.columns.

## Basics

- advanced compresion
- doesn't require indexes nor materialized views.
- massive parallel processing (MPP)
- columnar data storage (less I/Os)

## Cluster

- a single node has 160Gb
- a multi-node solution can be up to 128 nodes. Consists on a leader node and compute nodes.
- not multi-az. only available on 1 AZ. (Not available)

## Pricing

- billed per unit of process on a node on a hour
- not charged for the leader
- backups
- data transfer

## Encryption

- in-transit SSL. EASE-256 enc.
- redshift takes care of key management
    - integration with KMS
    - integration with HSM

## Backups

- can be moved to different AZs
