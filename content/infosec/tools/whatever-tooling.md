# Pentesting tooling
```bash
# assetfinder github.com/tomnomnom/assetfinder
assetfinder uber.com

# httprobe - test ssl/tls - github.com/tomnomnom/httprobe
cat domains.txt | httprobe

# gron - parse json files - github.com/tomnomnom/gron
curl -s http://headers.jsontest.com/ | gron

# meg - requets urls from a txt input and endpoints from another txt file - github.com/tomnomnom/meg
meg --verbose paths.txt hosts.txt

# unfurl - decompose urls by domain, endpoints, keypairs, etc - github.com/tomnomnom/unfurl
cat urls.txt | unfurl keypairs

# wfuzz - fuzz paths, get/post requests,   etc
wfuzz -w /usr/share/wfuzz/wordlist/general/common.txt --hc 404 ht

# dictionaries: /usr/share/<app>
fuzzdb, seclists

# whatweb
whatweb

# wappalyzer cli
webanalyze -host www.obmedia.com -crawl 3

# DNS online enumeration
sublist3r -d grammarly.com

# Cracking
john $FILE --format-descryp
```
# Pentesting tooling


## Infosec

```bash
# Identify type of a hash
hashid | hashtag

# intercept and analyze http traffic
 _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=gasp' burpsuite &

# assetfinder
# go get -u github.com/tomnomnom/assetfinder
assetfinder uber.com

# httprobe - test ssl/tls
# go get -u github.com/tomnomnom/httprobe
cat domains.txt | httprobe

# gron - parse json files
# go get -u github.com/tomnomnom/gron
curl -s http://headers.jsontest.com/ | gron

# meg - requets urls from a txt input and endpoints from another txt file
# go get -u github.com/tomnomnom/meg
meg --verbose paths.txt hosts.txt

# unfurl - decompose urls by domain, endpoints, keypairs, etc
# go get -u github.com/tomnomnom/unfurl
cat urls.txt | unfurl keypairs

# wfuzz - fuzz paths, get/post requests,   etc
wfuzz -w /usr/share/wfuzz/wordlist/general/common.txt --hc 404 ht

# dictionaries: /usr/share/<app>
fuzzdb, seclists

# unknown and interesting tools
whatweb

# wappalyzer cli
webanalyze -host https://xtime.com

# Identify type of a hash
hashid | hashtag

# intercept and analyze http traffic
 _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=gasp' burpsuite &

# assetfinder
# go get -u github.com/tomnomnom/assetfinder
assetfinder uber.com

# httprobe - test ssl/tls
# go get -u github.com/tomnomnom/httprobe
cat domains.txt | httprobe

# gron - parse json files
# go get -u github.com/tomnomnom/gron
curl -s http://headers.jsontest.com/ | gron

# meg - requets urls from a txt input and endpoints from another txt file
# go get -u github.com/tomnomnom/meg
meg --verbose paths.txt hosts.txt

# unfurl - decompose urls by domain, endpoints, keypairs, etc
# go get -u github.com/tomnomnom/unfurl
cat urls.txt | unfurl keypairs

# wfuzz - fuzz paths, get/post requests,   etc
wfuzz -w /usr/share/wfuzz/wordlist/general/common.txt --hc 404 ht

# dictionaries: /usr/share/<app>
fuzzdb, seclists

# unknown and interesting tools
whatweb

# wappalyzer cli
webanalyze -host https://xtime.com

# DNS online enumeration
sublist3r -d grammarly.com

wfuzz --hc 403 -c -w subdomains-top1mil-5000.txt -H "HOST: FUZZ.player.htb" http://10.10.10.145
gobuster dir -u http://player.htb/ -w /usr/share/wordlists/dirb/common.txt 
masscan -p1-65535 10.10.10.145 --rate=1000 -e tun0
gobuster dir -u http://dev.player.htb/ -w /usr/share/wordlists/dirb/common.txt 
stty raw -echo && nc -lvnp 1337
```
