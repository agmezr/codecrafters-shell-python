import sys
import os
import subprocess
from pathlib import Path

def _print(s):
    sys.stdout.write(f"{s}\n")

def _exit(*_):
    exit()

def _type(*args):
    t = args[0]
    if t in COMMANDS:
        _print(f"{t} is a shell builtin")
    else:
        path = get_path(t)
        if not path:
            _print(f"{t}: not found")
        else:
            _print(f"{t} is {path}")

def _pwd(*_):
    _print(os.getcwd())


def _cd(*args):
    p = args[0]
    if p.startswith("~"):
        home = Path.home()
        p = home + p[1:]
    try:
        os.chdir(p)
    except:
        _print(f"cd: {p}: No such file or directory")


def _echo(*args):
    txt = " ".join(args)
    sys.stdout.write(f"{txt}\n")

COMMANDS = {
    "echo": _echo,
    "exit": _exit,
    "type": _type,
    "pwd": _pwd,
    "cd": _cd,
}



def get_path(cmd: str):
    paths = os.getenv('PATH').split(os.pathsep)
    for path in paths:
        cmd_path = os.path.join(path, cmd)
        if os.access(cmd_path, os.X_OK):
            return cmd_path
    return None


def main():
    while True:
        sys.stdout.write("$ ")
        line = input()
        txt = line.split(" ")
        cmd = txt[0]
        args = txt[1:]
        if cmd in COMMANDS:
            fn = COMMANDS[cmd]
            fn(*args)
        else:
            path = get_path(cmd)
            if path:
                res = subprocess.run([cmd, *args], capture_output=True, text=True)
                _print(res.stdout.rstrip())
            else:   
                sys.stdout.write(f"{cmd}: command not found \n")
    

if __name__ == "__main__":
    main()
