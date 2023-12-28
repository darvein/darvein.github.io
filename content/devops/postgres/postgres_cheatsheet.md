# Postgresql general cheatsheet

## General

```sql
\dt   # list all tables
\l    # list all databases
\d    # describe table
```

```bash
#ssh jumpbox:
ssh -i ~/.ssh/devops-synapbox.pem -N -L 5432:synapbox-dev-postgresql.cluster-ro-cxt0zmlbsvfo.us-west-2.rds.amazonaws.com:5432 ec2-user@52.24.146.217
```

## Export and import database

```bash
pg_dump -h $HOST -U $USER -W -F t $DBNAME > dump.tar
pg_restore -h $HOST -d $DBNAME dump.tar -c -U $USER
```

## Misc

```bash
# create user and database
sudo su - postgres
createuser dennis
createdb -O dennis dennis

# test user
psql -h localhost -d dennis -U dennis -W
psql -h localhost -d postgres -U postgres -W
psql -h 192.168.56.181 -d dennis -U dennis -W

psql -h 54.212.233.131 -d postgres -U postgres -W
drop schema av2sch CASCADE;
drop user av2user;

# set superuser permissions
ALTER USER dennis WITH SUPERUSER;

# set privileges schema to user
ALTER DEFAULT PRIVILEGES IN SCHEMA av2sch GRANT SELECT ON TABLES TO dennis;

ALTER DEFAULT PRIVILEGES IN SCHEMA foo GRANT SELECT ON TABLES TO staff;
ALTER DEFAULT PRIVILEGES IN SCHEMA foo REVOKE ...;

ALTER DEFAULT PRIVILEGES FOR ROLE my_creating_role IN SCHEMA foo GRANT ...;
ALTER DEFAULT PRIVILEGES FOR ROLE my_creating_role IN SCHEMA foo REVOKE ...;

# set user password
vim /etc/postgresql/9.3/main/pg_hba.conf
#local      all              postgres                                peer
#local      all              postgres                                md5

ALTER USER "user_name" WITH PASSWORD 'new_password';
ALTER USER username WITH ENCRYPTED PASSWORD 'password';
ALTER USER "postgres" WITH PASSWORD 'mypassword';

# Remove
apt-get -y remove --purge postgres*
sudo rm -rf /var/lib/postgresql/
sudo rm -rf /var/log/postgresql/
sudo rm -rf /etc/postgresql/

# show tables
\dt av2sch.*

# drop schema
DROP schema av2sch CASCADE;
```

```sql
CREATE ROLE developers;

GRANT USAGE ON SCHEMA public to developers;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO developers;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO developers;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO developers;

CREATE USER luisrivera WITH PASSWORD 'jH529kn0IAQWy+mDgErj4w';
CREATE USER juansolano WITH PASSWORD 'yR2TSd0T5nu0GalT1rPtHw';
GRANT developers TO luisrivera;
GRANT developers TO juansolano;
```

postgresql with docker

```
docker run --name postgresql-master -p 5432:5432 \
  -e POSTGRESQL_REPLICATION_MODE=master \
  -e POSTGRESQL_USERNAME=my_user \
  -e POSTGRESQL_PASSWORD=password123 \
  -e POSTGRESQL_DATABASE=my_database \
  -e POSTGRESQL_REPLICATION_USER=my_repl_user \
  -e POSTGRESQL_REPLICATION_PASSWORD=my_repl_password \
  bitnami/postgresql:latest
```
