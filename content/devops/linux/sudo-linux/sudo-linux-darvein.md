# Sudo resume

- Sudo is a program that allow an user to run a command as another user, usually superuser
- `sudo` is not `su`, sudo requires user's password
- `sudo` activities are logged in systemd (journalctl)
- By default sudo invocation rights last **5 minutes**
- openbsd has **doas**, windows as **runas**

# /etc/sudoers

Config file is located at */etc/sudoers*. The tool *visudo* edits sudoers file in a safe manner: syntax check and locks

**Aliases:**
```
Host_Alias  SRV = black.com, smokie.com, frankie.com
User_Alias  WEBADMIN = ankit, sam
Cmnd_Alias  HTTPD = /usr/bin/httpd, /usr/bin/mysql
Cmnd_Alias  REBOOT = /sbin/halt, /sbin/reboot, \
                     /sbin/poweroff
Runas_Alias OP = root, operator
```

---

**Sudo assignation:**

```
#user1   host = (user2) command
WEBADMIN SRV  = (OP)    HTTPD, REBOOT, !/sbin/halt
%wheel   ALL  = (ALL)   NOPASSWD: ALL
```
---

**What accesss do we have?**
```
$ sudo -l
User foobar may run the following commands on shine:
    (n0kt, root) /home/n0kt/talks/sudo-linux/demo.sh
```

# sudoreplay

It allow us to audit and replay any sudo activity:

- It has to be enabled in /etc/sudoers
- Then we can play with `sudo sudoreplay` to explore sudo executions and outputs

---

```bash
~» sudo whoami
root


~» sudo sudoreplay -l user n0kt
...USER=root;HOST=shine;TSID=00/00/01;COMMAND=/bin/ifconfig
...USER=root;HOST=shine;TSID=00/00/02;COMMAND=/bin/whoami


~» sudo sudoreplay 00/00/02
Replaying sudo session: /bin/whoami
root
```

# Sudo best practices

- Default secure $PATH (so user don't override it)
```
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

# Demo

Simple demo!

# CVEs!

- CVE-2021-3156 before 1.9.5p2 version: 
```
sudo -s '\\' `perl -e 'print "A" x 65536'`
sudoedit -s '\' `perl -e 'print "A" x 65536'`
```

# More information

- Webpage: [https://www.sudo.ws/sudo/](https://www.sudo.ws/sudo/)
- Source code: [https://github.com/sudo-project/sudo](https://github.com/sudo-project/sudo)
- Principal maintainer: 
  - linkedin: Todd Miller [https://www.linkedin.com/in/millert/](https://www.linkedin.com/in/millert/)
  - twitter: [https://twitter.com/indieami](https://twitter.com/indieami)
