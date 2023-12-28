#  Bash training - Day 2

## Bash variables and programming structures



### Variables

Basic variables definition:

```bash
$ cat 01.sh
#!/bin/bash
name="Lobo López"
echo "Hello ${name}"
echo -e "\e[1;31mbye bye"

$ ./01.sh
Hello Lobo López
bye bye
```

Defaulting parameters:

```bash
$ cat 01.sh
#!/bin/bash

domain="${1:-industrialmurillo.edu.bo}"
echo "Checking ${domain}"

dig +short ns $domain \
          | xargs -I {} dig +short axfr "${domain}" "@{}"


$ ./01.sh aeumsa.edu.bo
Checking aeumsa.edu.bo
serv1.aeumsa.edu.bo. root.aeumsa.edu.bo. 113411 604800 86400 2419200 604800
serv1.aeumsa.edu.bo.
200.7.160.154
serv1.aeumsa.edu.bo.
173.254.79.187
serv1.aeumsa.edu.bo.
200.7.160.154
serv1.aeumsa.edu.bo.
200.7.160.154
serv1.aeumsa.edu.bo. root.aeumsa.edu.bo. 113411 604800 86400 2419200 604800
```

### Special variables

Useful list of bash special variables:

```bash
$#		# Number of input parameters separated by space
$0		# Name of the executed file
$1-$9 	# Input parameters
$$		# Process ID of the current shell
$?		# Last command exit status code
$!		# Process ID of the last background job
$@		# Store into an array all input parameters
$*		# String join of all input parameters into one string
```

### Conditionals

```bash
$ cat 02.sh
#!/bin/bash

while read url; do
  webserver=$(curl -sI "${url}" | grep -i Server)

  if [[ $webserver == *"Apache/"* ]]; then
    echo "[+] Apache found at: ${url} checking security..."
  elif [[ $webserver == *"nginx/"* ]]; then
    echo "[+] Nginx found at: ${url} checking security..."
  else
    echo "-> Not exploitable $url uses: ${webserver}"
  fi
done < $1


$ ./02.sh list.txt
-> Not exploitable https://www.umsa.bo/ uses: Server: Apache-Coyote/1.1
-> Not exploitable https://fment.umsa.bo/ uses: Server: Apache-Coyote/1.1
-> Not exploitable https://gestiones.umsa.bo/ uses: Server: Apache-Coyote/1.1
[+] Apache found at: http://cmat.umsa.bo/ checking security...
[+] Apache found at: https://miing.umsa.edu.bo/ checking security...
[+] Apache found at: http://titulos.umsa.bo/ checking security...
[+] Apache found at: http://www.faadu.umsa.bo/wp/ checking security...
-> Not exploitable https://ft.umsa.bo/ uses: Server: Apache-Coyote/1.1
[+] Apache found at: http://fo.umsa.bo/ checking security...
-> Not exploitable https://economia.umsa.bo/ uses: Server: Apache-Coyote/1.1
-> Not exploitable https://www.umsa.bo/web/carrera-de-bibliotecologia uses: Server: Apache-Coyote/1.1
[+] Apache found at: http://recursoshumanos.umsa.bo/ checking security...
[+] Apache found at: http://postgrado.fment.umsa.bo/ checking security...
[+] Apache found at: http://www.informatica.umsa.bo/ checking security...
-> Not exploitable https://transparencia.umsa.bo/ uses: Server: Apache-Coyote/1.1
```

Comparison operators:

| **Operator** | **Description**                                         |
| ------------ | ------------------------------------------------------- |
| -eq          | Returns true if two numbers are equivalent              |
| -lt          | Returns true if a number is less than another number    |
| -gt          | Returns true if a number is greater than another number |
| ==           | Returns true if two strings are equivalent              |
| !=           | Returns true if two strings are not equivalent          |
| !            | Returns true if the expression is false                 |
| -d           | Check the existence of a directory                      |
| -e           | Check the existence of a file                           |
| -r           | Check the existence of a file and read permission       |
| -w           | Check the existence of a file and write permission      |
| -x           | Check the existence of a file and execute permission    |

```bash
$ cat 02.sh
#!/bin/bash

mkdir /root/foo
if [[ $? -ne 0 ]]; then
        echo "Failed to create directory"
fi


$ ./02.sh
mkdir: cannot create directory ‘/root/foo’: Permission denied
Failed to create directory
```



### Loops



```bash
bob@worker:~/day1$ cat 03.sh
#!/bin/bash

cd terraform-aws-rds
for f  in $(find . -type f -not -path '*/\.git/*'); do
  data=$(git log -1 --pretty="format:(%ae) %ci" $f)
  echo "-> ${data} ${f}"
done | column -t | sort -k3


$ ./03.sh  | tail -n 10
->  (48199696+stefan-matic@users.noreply.github.com)        2022-05-27  18:21:18  +0200  ./examples/cross-region-replica-postgres/outputs.tf
->  (48199696+stefan-matic@users.noreply.github.com)        2022-05-27  18:21:18  +0200  ./examples/enhanced-monitoring/README.md
->  (48199696+stefan-matic@users.noreply.github.com)        2022-05-27  18:21:18  +0200  ./examples/enhanced-monitoring/outputs.tf
->  (48199696+stefan-matic@users.noreply.github.com)        2022-05-27  18:21:18  +0200  ./examples/replica-mysql/README.md
->  (48199696+stefan-matic@users.noreply.github.com)        2022-05-27  18:21:18  +0200  ./examples/replica-mysql/outputs.tf
->  (48199696+stefan-matic@users.noreply.github.com)        2022-05-27  18:21:18  +0200  ./examples/replica-postgres/README.md
->  (48199696+stefan-matic@users.noreply.github.com)        2022-05-27  18:21:18  +0200  ./examples/replica-postgres/outputs.tf
->  (48199696+stefan-matic@users.noreply.github.com)        2022-05-27  18:21:18  +0200  ./examples/s3-import-mysql/outputs.tf
->  (48199696+stefan-matic@users.noreply.github.com)        2022-05-27  18:21:18  +0200  ./outputs.tf
->  (69353814+riccardo-salamanna@users.noreply.github.com)  2021-07-07  17:31:36  +0300  ./examples/cross-region-replica-postgres/variables.tf

```

## Essential tools you need to know Part 2

```bash
ubuntu@ip-172-31-95-65:~$ whatis sort uniq find cut awk sed tr xargs which
sort (1)             - sort lines of text files
uniq (1)             - report or omit repeated lines
find (1)             - search for files in a directory hierarchy
cut (1)              - remove sections from each line of files
awk (1)              - pattern scanning and processing language
sed (1)              - stream editor for filtering and transforming text

tr (1)               - translate or delete characters
xargs (1)            - build and execute command lines from standard input
which (1)            - locate a command
```

