# Mysql tips



**Create user in AWS RDS and grant permissions like a master**

```bash

CREATE USER 'jacob'@'%' IDENTIFIED BY 'xxxxxxxx';
GRANT SELECT,INSERT,UPDATE,DELETE,DROP on synapbox_qa.* TO 'jacob'@'%';

or

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, PROCESS, REFERENCES, INDEX, ALTER, SHOW DATABASES, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER, LOAD FROM S3, SELECT INTO S3, INVOKE LAMBDA ON synapbox_qa.* TO 'jacob'@'%' IDENTIFIED BY PASSWORD WITH GRANT OPTION

```



#### Need to check all the queries in live mode?:

```sql
mysql> SHOW VARIABLES LIKE "general_log%";
+------------------+----------------------------+
| Variable_name    | Value                      |
+------------------+----------------------------+
| general_log      | OFF                        |
| general_log_file | /var/run/mysqld/mysqld.log |
+------------------+----------------------------+

mysql> SET GLOBAL general_log = 'ON';
mysql> SET GLOBAL general_log = 'OFF';
```

#### Check size in disk on each table:

```sql
SELECT 
     table_schema as `Database`, 
     table_name AS `Table`, 
     round(((data_length + index_length) / 1024 / 1024), 2) `Size in MB` 
FROM information_schema.TABLES 
ORDER BY (data_length + index_length) DESC;
```

#### SSH Mysql tunnel

```bash
# RDS Mysql
ssh -t -N -L 3306:acmeorgdb-staging.cluster-xxxxxx.us-east-1.rds.amazonaws.com:3306 -i ~/.ssh/acmeorg-devops.pem ubuntu@$HOST
# then in a new terminal
mysql -h 127.0.0.1 -u dbuser -p
```

#### Check collation

```sql
SHOW VARIABLES LIKE '%collation%';
```



#### Others

```mysql
# check how to create an existing table
show create table serpTermStrategy
```





## Good to know

- `mysqldump` can dump data and compress it with different algorithms and levels of preset.

