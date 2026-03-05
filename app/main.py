import sys
import os
import subprocess
from pathlib import Path
import shlex

from app import utils

class ShellException(Exception):
    ...

def _print(s):
    if not s:
        return
    sys.stdout.write(f"{s}\n")

def _exit(*_):
    exit()

def _type(*args):
    t = args[0]
    if t in COMMANDS:
        return f"{t} is a shell builtin"
    else:
        path = get_path(t)
        if not path:
            raise ShellException(f"{t}: not found")
        else:
            return f"{t} is {path}"

def _pwd(*_):
    _print(os.getcwd())


def _cd(*args):
    p = args[0]
    if p.startswith("~"):
        home = Path.home()
        p = os.path.join(home, p[1:])
    try:
        os.chdir(p)
    except:
        raise ShellException(f"cd: {p}: No such file or directory")


def _echo(*args):
    return " ".join(args) 

def _cat(*args):
    txt = " ".join(args)
    tokens = utils.split_tokens(txt)
    for path in tokens:
        p = Path(path)
        if not p.exists():
            _print(f"cat: {p}: No such file or directory")
        if p.is_dir():
            _print(f"cat: {p}: Is a directory")
        with p.open() as f:
            t = f.read()
            sys.stdout.write(f"{t}")

COMMANDS = {
    "echo": _echo,
    "exit": _exit,
    "type": _type,
    "pwd": _pwd,
    "cd": _cd,
    #"cat": _cat,
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
        if not line:
            continue
        txt = shlex.split(line)
        cmd = txt[0]
        args = txt[1:]
        output = None

        mode, index = utils.find_redirect(args)
        if mode > 0:
            output = args[-1]
            args = args[:index]
            _path = Path(output)
            _path.parent.mkdir(parents=True, exist_ok=True)
            _path.touch()

        if cmd in COMMANDS:
            fn = COMMANDS[cmd]
            try:
                result = fn(*args)
                if mode == 1:
                    utils.to_file(output, result)
                else:
                    _print(result)
            except ShellException as e:
                if mode == 2:
                    utils.to_file(output, result)
                else:
                    _print(e)

        else:
            path = get_path(cmd)
            if path:
                res = subprocess.run([cmd, *args], capture_output=True, text=True)
                if mode == 1:
                    utils.to_file(output, res.stdout)
                else:
                    _print(res.stdout.rstrip())
                if res.stderr:
                    if mode == 2:
                        utils.to_file(output,res.stderr)
                    else:
                        sys.stdout.write(res.stderr)                    
            else:   
                sys.stdout.write(f"{cmd}: command not found \n")
    

if __name__ == "__main__":
    main()
