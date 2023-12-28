# Blackbox

# smashthestack.org blackbox
ssh -l level1 blackbox.smashthestack.org -p 2225

**Level1**
ssh -l level1 blackbox.smashthestack.org -p 2225
```
level1@blackbox:~$ strings login2
...
PassFor2
...
level1@blackbox:~$ ./login2
Access Code: PassFor2
sh-3.1$
b0wer:~ tenazas$ ssh -l level2 blackbox.smashthestack.org -p 2225
level2@blackbox.smashthestack.org's password:
Last login: Tue Jan 22 23:28:24 2019 from 213.91.183.174
```
**Level2**
ssh -l level1 blackbox.smashthestack.org -p 2225
```
```
**Level3**
**Level4**



#bugbounty/smashthestack
