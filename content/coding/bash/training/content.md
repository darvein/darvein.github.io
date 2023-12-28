# Bash Scripting Training Content

### Day 1
- Linux basics
- Bash introduction
- Essential tools you need to know
- List of commands

### Day 2
- Special variables
  - $#, $0, $n, $$, $?, $!, $@/$*
- Arrays
- Programming Structures
- Essential tools you need to know - Part 2
  - sort, uniq, find, cut, awk, sed
  - tr, xargs, which

### Day 3
- Redirections
  - stdin, stdout, stderr, tee, /dev/null, /dev/fd/0
  - /dev/stdin, /dev/tcp/host/port
- Functions
  - Bash export functions 
  - Declare -fx foo
- Pipes
- Status and Exit codes
  - 0 and 255
  - syscall responder `waitpid`
- Error management and debugging
  - -eux, trap, echos
  - --debugger (bashdb)

### Day ?
- Math
  - Calculations with bc 
  - Convert oct, hexa to dec
  - Declare -i 16 i=255 
  - Declare -F 3 x='1.0/3' # or -E 
- Jobs
  - jobs, fg, bg
  - Jobs, ctrl z, fg %1, bg %1, stop %1 
- Shell expansions
  - REVIEW: https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#Special-Parameters
  - Brace expansion: mkdir ~/tmp/{a,b,c}.txt
  - Parameter expansion: ${var:=default}, ${var:?var is unset or null}
  - Parameter offsets: ${parameter:offset:length}
  - Patterns
    - User ${HOME##*/} or %% vs ##
  - Expanders
    - Expansion flags: uppercase 
    - Mv $f ${(L)f} 
    - Strings management
      - A=1234567890
      - ${A:2:3}
  - Braces multiple options, gen numbers, alphabet, 
- Groups and subshells
  - <() >() $() 
  - () vs {}
  - {Sleep 5; make; } &
- Bash autocompletion

Labs:
- Cool bash functions:
  - Most big files or directories function
  - Most consuming mem app
- Aws cli jq: list users
- Gcloud yq: list instances
- Docker cli cleanup
- Git: tricks
- Extract parse html data: curl
  - Curl and JSON payloads
- FFmpeg:
  - YouTube dl 
  - Convert mp4 to mp3 ffmpeg
  - Compress images
- Nmap ssl lib?, openssl cli download certificate

Others:
- Signals
- ulimit
- POSIX

Complementary:
- Bash builtin functiosn

### Resources
- https://www.learnshell.org/en/Special_Variables
- https://tldp.org/LDP/Bash-Beginners-Guide/html/Bash-Beginners-Guide.html
- https://devdocs.io/bash/
- https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html
