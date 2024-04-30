import os
import sys
import subprocess

PROGRAM      = sys.argv[1]
INFILE       = PROGRAM.split(".")[0] + ".in"
OUTFILE      = PROGRAM.split(".")[0] + ".out"
EXTENSION    = PROGRAM.split(".")[-1]
PROGRAM_NAME = PROGRAM.split(".")[0]

def call_cmd(cmd):
    try:
        return subprocess.call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)

def run_cmd(cmd):
    ret = None;
    try:
        ret = subprocess.check_output(cmd, shell=True).decode('utf-8')
        print(ret)
    except subprocess.CalledProcessError as e:
        print(e.output.decode('utf-8'))
    return ret

def check_result(ret):
    if not os.path.exists(OUTFILE): return
    with open(OUTFILE) as expected:
        if ret == expected.read():
            print("[+] All results are good!")
        else:
            print("[-] Results not expected!")

def gen_cmd(cmd):
    if os.path.exists(INFILE):
        return "cat {} | {}".format(INFILE, cmd)
    return cmd

def run_cpp():
    cmd = "/usr/bin/g++ -g -std=c++17 -C -W -Wall -pedantic {}".format(PROGRAM)
    ret = call_cmd(cmd)

    if ret != 0:
        print("[-] Compilation failed!")
        sys.exit(0)

    if os.path.exists(INFILE):
        cmd = "cat {} | ./a.out".format(INFILE)
        check_result(run_cmd(gen_cmd(cmd)))
    else:
        run_cmd("./a.out")

    # Cleanup
    if os.path.exists('a.out'): os.remove("a.out")

def run_java():
    # Main.class  Multiply.class  Multiply.java
    cmd = "javac {}".format(PROGRAM)
    ret = call_cmd(cmd)

    if ret != 0:
        print("[-] Compilation failed!")
        sys.exit(0)

    if os.path.exists(INFILE):
        # cmd = "cat {} | java {}".format(INFILE, PROGRAM_NAME)
        cmd = "cat {} | java {}".format(INFILE, "Main")
        check_result(run_cmd(gen_cmd(cmd)))
    else:
        # run_cmd("java {}".format(PROGRAM_NAME))
        run_cmd("java {}".format("Main"))

    # Cleanup
    if os.path.exists('a.out'): os.remove("a.out")

def run_program():
    if EXTENSION   == "go": cmd = gen_cmd("go run {}".format(PROGRAM))
    elif EXTENSION == "py": cmd = gen_cmd("python {}".format(PROGRAM))
    elif EXTENSION == "sh": cmd = gen_cmd("/bin/bash {}".format(PROGRAM))
    elif EXTENSION == "js": cmd = gen_cmd("node {}".format(PROGRAM))
    elif EXTENSION == "php": cmd = gen_cmd("php {}".format(PROGRAM))
    elif EXTENSION == "rb": cmd = gen_cmd("ruby {}".format(PROGRAM))
    elif EXTENSION == "ps1": cmd = gen_cmd('docker run -v "{}:/app" mcr.microsoft.com/powershell /app/{}'.format(os.getcwd(), PROGRAM))

    else: sys.exit(0)

    ret = run_cmd(gen_cmd(cmd))
    check_result(ret)

if __name__ == "__main__":
    if EXTENSION == "cpp":
        run_cpp()
    if EXTENSION == "java":
        run_java()
    else:
        run_program()
