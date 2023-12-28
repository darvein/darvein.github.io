# Chapter 3

## System has users and groups

Everything is a file: processes, devices, network connections and have uid/gid

root is always 0, gid 0, users starts from 1000

su != sudo

## setuid and setgid

setuid and setgid: Runs with pre-defined uid/gid instead of the runner user's uid/gid
https://www.geeksforgeeks.org/setuid-setgid-and-sticky-bits-in-linux-file-permissions/

## sudo

/etc/sudoers

sudoreplay
Defaults log_output
Defaults!/usr/bin/sudoreplay !log_output
Defaults!/sbin/reboot !log_output
visudo

Disable root account with /bin/false /bin/nonlogin on /etc/passwd

## PAM

PAM: single-signon
Kerberos: network crypto auth (part of AD)

## Linux capabilities

## Linux namespaces

## AppArmor (canonical), Smack, TOMOYO, Yama, SELinux

## MAC Mandatory access control

## Others

https://www.thegeekdiary.com/understanding-the-etc-skel-directory-in-linux/
https://www.maketecheasier.com/check-sudo-history-linux/
https://www.redhat.com/sysadmin/pluggable-authentication-modules-pam
https://www.vultr.com/docs/working-with-linux-capabilities/


## Umask

Umask permissions

![image-20221118140813982](../../../images/articles/ch2/image-20221118140813982.png)
