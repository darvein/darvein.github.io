# easy - Codify

## User flag
So we start with the basics
```bash
~➤ sudo nmap -n -Pn -sV -O -T4 codify.htb
...
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.52
3000/tcp open  http    Node.js Express framework
...
```
Port 80 says they use a nodejs app where the following libs are being used:
- https://github.com/patriksimek/vm2/releases/tag/3.9.16

### The editor
Basically, the /editor page can run some javascript:
```bash
curl -s 'http://codify.htb/run' \
	-X POST \
	-H 'Referer: http://codify.htb/editor' \
	-H 'Content-Type: application/json' \
	--data-raw '{"code":"dmFyIGZvbz0xOwpjb25zb2xlLmxvZyhmb28pOw=="}'

The host under http://codify.htb:3000/run can also do the same, but it is just a sandbox.

# Result
# {"output":"1\r\n"}

# What is that `code` b64?:
# echo "dmFyIGZvbz0xOwpjb25zb2xlLmxvZyhmb28pOw==" | base64 -d
# var foo=1;
# console.log(foo);
```

## Root flag

## TODOs
