# Overthewire Leviathan

## info

SSH: ssh -p 2223 leviathan.labs.overthewire.org -l leviathan0
Passwords: /etc/leviathan_pass

## 0->1

```
leviathan0@leviathan:~$ grep -i pass .backup/bookmarks.html
<DT><A HREF="http://www.goshen.edu/art/ed/teachem.htm" ADD_DATE="1146092098" LAST_CHARSET="ISO-8859-1" ID="98012771">Pass it
<DT><A HREF="http://leviathan.labs.overthewire.org/passwordus.html | This will be fixed later, the password for leviathan1 is rioGegei8m" ADD_DATE="1155384634" LAST_CHARSET="ISO-8859-1" ID="rdf:#$2wIU71">password to leviathan1</A>
```

## 1->2

```
leviathan1@leviathan:~$ ls -la check
-r-sr-x--- 1 leviathan2 leviathan1 7452 Aug 26  2019 check

leviathan1@leviathan:~$ ltrace ./check
__libc_start_main(0x804853b, 1, 0xffffd794, 0x8048610 <unfinished ...>
printf("password: ")                                                                                       = 10
getchar(1, 0, 0x65766f6c, 0x646f6700password: foo
)                                                                      = 102
getchar(1, 0, 0x65766f6c, 0x646f6700)                                                                      = 111
getchar(1, 0, 0x65766f6c, 0x646f6700)                                                                      = 111
strcmp("foo", "sex")                                                                                       = -1
puts("Wrong password, Good Bye ..."Wrong password, Good Bye ...
)                                                                       = 29
+++ exited (status 0) +++

leviathan2@leviathan:~$ cat /etc/leviathan_pass/leviathan2
ougahZi8Ta
```

## 2->3

```
leviathan2@leviathan:~$ ls -ltra printfile
-r-sr-x--- 1 leviathan3 leviathan2 7436 Aug 26  2019 printfile

# symlink?
```
