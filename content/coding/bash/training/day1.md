# Bash training - Day 1

## Linux basics

Quick and simple intro to GNU/Linux.

### Directories and files on Linux

![image-20221009232820629](../../../../images/articles/day1/image-20221009232820629.png)

What type of files exist on Linux?

| Symbol | Meaning      |
| :----- | ------------ |
| -      | Regular file |
| d      | Directory    |
| l      | Link         |
| c      | Special file |
| s      | Socket       |
| p      | Named pipe   |
| b      | Block device |

Linux filesystem:

![image-20221009233809609](../../../../images/articles/day1/image-20221009233809609.png)

Comparing two directories:

```bash
$ diff -q a b
Files a/1.txt and b/1.txt differ
Only in b: 3.txt
Only in b: 4.txt
Only in b: 5.txt
```



### Processes

Listing current processes

```bash
$ ps aux | head
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  1.3 168756 13524 ?        Ss   03:07   0:01 /sbin/init
root           2  0.0  0.0      0     0 ?        S    03:07   0:00 [kthreadd]
root           3  0.0  0.0      0     0 ?        I<   03:07   0:00 [rcu_gp]
root           4  0.0  0.0      0     0 ?        I<   03:07   0:00 [rcu_par_gp]

...stripped...

$ file /sbin/init
/sbin/init: symbolic link to /lib/systemd/systemd
```

Own user processes:

```bash
$ ping google.com
PING google.com (142.251.0.102) 56(84) bytes of data.
64 bytes from cj-in-f102.1e100.net (142.251.0.102): icmp_seq=1 ttl=63 time=73.1 ms
^Z
[1]+  Stopped                 ping google.com

$ ps -L
    PID     LWP TTY          TIME CMD
   1805    1805 pts/0    00:00:00 bash
   2702    2702 pts/0    00:00:00 ping
   2703    2703 pts/0    00:00:00 ps
   
$ fg
# Press CTRL-C to finish ping
```



### Users, Permissions and Onwership

Who am I?

```bash
$ id
uid=1002(bob) gid=1002(bob) groups=1002(bob),27(sudo)
$ whoami
bob
```

Can I read what is not mine?

```bash
$ ls -l private.txt
-rw-r----- 1 root root 3 Oct 10 04:46 private.txt
$ cat private.txt
cat: private.txt: Permission denied
```

Can I execute a file that has no execution permission?

```bash
$ cat hello.sh
#!/bin/bash
echo "Hello World!"

$ ./hello.sh
bash: ./hello.sh: Permission denied

$ chmod +x ./hello.sh
$ ./hello.sh
Hello World!
```

Structure of permissions:

###### ![image-20221010005205921](../../../../images/articles/day1/image-20221010005205921.png)

## Bash Introduction

Bash is a command language, it works as interactive and scripted.

![image-20221010005438776](../../../../images/articles/day1/image-20221010005438776.png)

What shell are we using?

```bash
vagrant@worker:~$ ps $$
    PID TTY      STAT   TIME COMMAND
   1805 pts/0    Ss     0:00 -bash
```

### Looking for help

```bash
$ help
GNU bash, version 5.2.0(1)-rc2 (x86_64-pc-linux-gnu)
These shell commands are defined internally.  Type `help' to see this list.
Type `help name' to find out more about the function `name'.
Use `info bash' to find out more about the shell in general.
Use `man -k' or `info' to find out more about commands not in this list.

...stripped...
```

Help page for `cd` command:

```bash
$ help cd
cd: cd [-L|[-P [-e]] [-@]] [dir]
    Change the shell working directory.

    Change the current directory to DIR.  The default DIR is the value of the
    HOME shell variable. If DIR is "-", it is converted to $OLDPWD.
    
...stripped...
```

Quick description of a tool?:

```bash
$ whatis nmap bash youtube-dl whatis
nmap (1)             - Network exploration tool and security / port scanner
bash (1)             - GNU Bourne-Again SHell
youtube-dl (1)       - download videos from youtube.com or other video platforms
whatis (1)           - display one-line manual page descriptions
```

Review the full manual page: `man bash`

### Binaries and built-in functions

Is it a builtin function or a binary?

```bash
$ type nmap
nmap is /usr/bin/nmap
$ type cd
cd is a shell builtin
```

Where are the binaries?

```bash
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

Why is it important to check a binary?

```bash
$ ssh(){ echo "pwned ${1}"; }
$ ssh bob@localhost
# results?

$ type ssh
ssh is a function
...stripped...

$ whereis -b ssh
ssh: /usr/bin/ssh /etc/ssh
```

### Customizing Bash

Change the bash prompt:

```bash
bob@worker:~$ export PS1="\w naruto $ "
~ naruto $ ls -ld tmp
drwxrwxr-x 2 bob bob 4096 Oct 10 05:14 tmp

~ naruto $ source .bashrc
bob@worker:~$
```

How to customize bash?

```bash
$ file .bashrc /etc/bash.bashrc
.bashrc:          ASCII text
/etc/bash.bashrc: ASCII text
```

## Essential tools you need to know

```bash
bob@worker:~$ whatis date ping ssh ss nmap ls mkdir find file grep cat head tail sudo history time vim
date (1)             - print or set the system date and time

ssh (1)              - OpenSSH remote login client
ping (8)             - send ICMP ECHO_REQUEST to network hosts
ss (8)               - another utility to investigate sockets
nmap (1)             - Network exploration tool and security / port scanner

ls (1)               - list directory contents
mkdir (1)            - make directories
mkdir (2)            - create a directory
find (1)             - search for files in a directory hierarchy

file (1)             - determine file type
grep (1)             - print lines that match patterns
cat (1)              - concatenate files and print on the standard output
head (1)             - output the first part of files
tail (1)             - output the last part of files

sudo (8)             - execute a command as another user
history (3readline)  - GNU History Library
time (1)             - run programs and summarize system resource usage

vim (1)              - Vi IMproved, a programmer's text editor
```

Some examples:

```bash
$ TZ=Ukraine date -d "+1 hours"
Mon Oct 10 06:54:34 Ukraine 2022
```

### List of commands

```bash
$ id; date
uid=1002(bob) gid=1002(bob) groups=1002(bob),27(sudo)
Mon Oct 10 06:00:23 Bolivia 2022

$ id & date
[1] 7500
Mon Oct 10 06:00:31 Bolivia 2022
uid=1002(bob) gid=1002(bob) groups=1002(bob),27(sudo)
[1]+  Done                    id

$ mkdir -p tmp && cd tmp
~/tmp$ 

$ mkdir /root/tmp || echo "Nope!"
mkdir: cannot create directory ‘/root/tmp’: Permission denied
Nope!
$ echo $?
0
```

