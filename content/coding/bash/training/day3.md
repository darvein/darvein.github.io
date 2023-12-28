#  Bash training - Day 3

## Redirections

- stdin, stdout, stderr, tee, /dev/null, /dev/fd/0
- /dev/stdin, /dev/tcp/host/port

Standard intput/output

```bash
$ file /dev/stdin
/dev/stdin: symbolic link to /proc/self/fd/0

$ file /dev/stdout
/dev/stdout: symbolic link to /proc/self/fd/1

$ file /dev/stderr
/dev/stderr: symbolic link to /proc/self/fd/2
```

Special files being used for pipeping

```bash
$ ls -ltra /proc/self/fd/0
lrwx------ 1 ubuntu ubuntu 64 Oct 13 20:54 /proc/self/fd/0 -> /dev/pts/0
$ ls -ltra /dev/pts/0
crw--w---- 1 ubuntu tty 136, 0 Oct 13 20:54 /dev/pts/0
```



Sending stdin and stdout to a file

```bash
$ find / -name ping > log.out 2>&1

$ cat log.out  | grep -v Permission
/snap/core18/2566/bin/ping
/snap/core18/2566/usr/share/bash-completion/completions/ping
/snap/core18/2538/bin/ping
/snap/core18/2538/usr/share/bash-completion/completions/ping
/snap/core20/1623/usr/bin/ping
/snap/core20/1623/usr/share/bash-completion/completions/ping
/snap/core20/1611/usr/bin/ping
/snap/core20/1611/usr/share/bash-completion/completions/ping
/usr/bin/ping
/usr/share/bash-completion/completions/ping
```



```bash
$ nc -nvlp 55555
```

```bash
$ cat > /dev/tcp/127.0.0.1/55555
hey
```

## Functions

```bash
$ cat test.sh
#!/bin/bash
hello () {
  yourname=${1:-none}
  echo "-> Hello: ${yourname}"
}

hello "Juarez"


$ ./test.sh
-> Hello: Juarez
```

Export function:

```bash
$ source test.sh
$ hello foo
-> Hello: foo
```

## Pipes

```bash
$ find . | grep \.tf | xargs -I {} wc -l {} | sort -h -k 1 | tail -n 5
201 ./examples/complete-mssql/main.tf
209 ./examples/complete-postgres/main.tf
225 ./examples/cross-region-replica-postgres/main.tf
375 ./modules/db_instance/variables.tf
513 ./variables.tf
```

## Error management and debugging

```bash
$ cat test.sh
#!/bin/bash
set -euxo pipefail
cat foo | wc -l
ping -c 1 google.com

$ ./test.sh
+ wc -l
+ cat foo
cat: foo: No such file or directory
0
```

```bash
$ cat test.sh
#!/bin/bash
set -Eeuo pipefail

notify() {
        echo "Something went wrong"
}

trap notify ERR
function func(){
        ls /root/
}
func

ubuntu@ip-172-31-95-65:~$ ./test.sh
ls: cannot open directory '/root/': Permission denied
Something went wrong
```



