# RDS

- Supports relational: SQL Server, Oracle, Mysql, Aurora, PostgreSQL, MariaDB
- Supports nosql: dynamodb
- Data warehousing: redshift (OLAP)
- Encryption is supported (only applies if the db is being created and encryption option is enabled)
- All RDS are OLTP

## Backups

- two types: automated backups and database snapshots
- automated backups: 
    - aws takes a full daily snapshots with a retention period of 35 days.
    - enabled by default
    - stored in s3
    - during the backup process, the db i/o may be suspended or increased latency may be seen
- database snapshots:
    - user initiazed
    - triggered when a db is deleted
    - the restore process creates a new RDS
    - snapshots can be encrypted

## Multi-AZ

- Databases are replicated to different AZs (subnets). DR only, not performance.

## Read Replica

- a way to scale a database cluster, the replicas are asynchronous copies of the main db.
- ready-heave workloads
- doesn't work with: SQL Server and Oracle
- for scaling, not DR
- automatic backups needed enabled
- limit of a 5 read replicas per db
- each read-replica have its own DNS endpoint
- read-replicas can have multi-az and/or different region
- read-replicas of multi-az source databases
- read-replicas can be promoted to its own database (write/read)

## Engine: Aurora

- mysql-compatible
- x5 times better performance than mysql ?
- starts with 10Gb, scales in 10Gb increments to 65Tb
- scales up to 32vcpus and 244Gb of mem
- 2 copies of data is maintained on each AZ, minimum of 3 AZs. 6 copies of the data.
- disks are automatically scaned and repaired
- replicas:
    - aurora replicas: 15 (failovers)
    - mysql read replicas: 5
- endpoints for both lead and replicas have the same endpoint (failover purposes)


## Engine: SQL Server

- For RDS IOPS provisioned storage, the maximum volume can be 32TB

## Limitations

- Don't use it for large binary objects (AWS S3 is an option)
- It doesn't scale automatically (dynamodb does)
- When data is not well structured or is unpredictable (use dynamodb)
- It doesn't support DB2 or HANA DB
- Not complete access to the underlying EC2 instances
