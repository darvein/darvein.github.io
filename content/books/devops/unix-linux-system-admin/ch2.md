# Chapter 2

This document is a summary of my own notes on this book.

## Boot process

Bootstrap process overview:

![image-20221110230441820](../../../images/articles/unix-linux-system-administration-handbook/image-20221110230441820.png)



### BIOS vs UEFI?

meh...

### Init

Variants?: SystemV init, SystemV upstart

Ubuntu 14 running `init`:

```bash
vagrant@worker:~$ ps -fp 1
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 03:46 ?        00:00:00 /sbin/init

vagrant@worker:~$ /sbin/init --version
init (upstart 1.12.1)
Copyright (C) 2006-2014 Canonical Ltd., 2011 Scott James Remnant
```

Exploring units:

```bash
root@worker:~$ ls /etc/init.d | grep nginx
nginx

root@worker:~$ /etc/init.d/nginx status
 * nginx is running

root@worker:~$ cat /run/nginx.pid
3334
```

Runlevels:

- Runlevel 0 is halt
- Runlevel 1 is single-user
- Runlevels 2-5 are multi-user (some distro uses RUN level 5 to start X [KDE/Gnome])
- Runlevel 6 is for rebooting system

```bash
root@worker:~$ runlevel
N 2

root@worker:~$ ls /etc/rc2.d/
README    S20rsync           S20virtualbox-guest-utils  S38open-vm-tools     S70dns-clean  S99chef-client  S99ondemand
S20nginx  S20screen-cleanup  S21puppet                  S45landscape-client  S70pppd-dns   S99grub-common  S99rc.local

root@worker:/home/vagrant$ init 0
root@worker:/home/vagrant$ Connection to 127.0.0.1 closed by remote host.
```



### Systemd

```bash
vagrant@worker:~$ ps -fp 1
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 04:13 ?        00:00:01 /sbin/init
vagrant@worker:~$ ls -ltra /sbin/init
lrwxrwxrwx 1 root root 20 Oct 11 15:51 /sbin/init -> /lib/systemd/systemd
```

Components:

![image-20221111001905442](../../../images/articles/unix-linux-system-administration-handbook/image-20221111001905442.png)

Exploring units:

```bash
vagrant@worker:/etc/systemd/system$ find .  | grep nginx
./multi-user.target.wants/nginx.service

vagrant@worker:/etc/systemd/system$ sudo systemctl list-unit-files --type=service | grep nginx
nginx.service                          enabled         enabled
```

Checking logs:

```bash
vagrant@worker:~$ sudo journalctl -u nginx.service --since=today
Nov 11 04:20:05 worker systemd[1]: Starting A high performance web server and a reverse proxy server...
Nov 11 04:20:05 worker systemd[1]: Started A high performance web server and a reverse proxy server.
```

Sample of nginx unit config:

```bash
[Unit]
Description=A high performance web server and a reverse proxy server
Documentation=man:nginx(8)
After=network.target nss-lookup.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/sbin/nginx -g 'daemon on; master_process on;' -s reload
ExecStop=-/sbin/start-stop-daemon --quiet --stop --retry QUIT/5 --pidfile /run/nginx.pid
TimeoutStopSec=5
KillMode=mixed

[Install]
WantedBy=multi-user.target
```

```bash
~» file /home/n0kt/.config/systemd/user/dropbox.service
/home/n0kt/.config/systemd/user/dropbox.service: ASCII text

~» systemctl --user status dropbox.service
● dropbox.service - Dropbox as a user service
     Loaded: loaded (/home/n0kt/.config/systemd/user/dropbox.service; enabled; preset: enabled)
     Active: active (running) since Fri 2022-11-11 00:32:19 -04; 1min 23s ago
   Main PID: 931791 (dropbox)
      Tasks: 94 (limit: 18885)
     Memory: 3.1G
        CPU: 2min 3.058s
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/dropbox.service
             └─931791 /home/n0kt/.dropbox-dist/dropbox-lnx.x86_64-161.4.4923/dropbox
```

Runlevels:

```bash
vagrant@worker:/etc/systemd$ systemctl get-default
graphical.target

vagrant@worker:/etc/systemd$ sudo systemctl isolate poweroff.target
Connection to 127.0.0.1 closed by remote host.
```

![image-20221111003828630](../../../images/articles/unix-linux-system-administration-handbook/image-20221111003828630.png)

### Controversies

- Problems with Opensource community and Linus
- "kerio" wanting to hire a hitman to kill Lennort https://logs.nslu2-linux.org/livelogs/maemo/maemo.20130215.txt

## Video discussions / Reviews

- Chapter 2: https://www.dropbox.com/s/o0225cdlcz42sxd/unix-book-c2.mp4?dl=0

{{< video-dropbox url="https://www.dropbox.com/s/o0225cdlcz42sxd/unix-book-c2.mp4?dl=0&dl=0&raw=1" >}}
