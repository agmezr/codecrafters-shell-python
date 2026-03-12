import sys
import os
import subprocess
from pathlib import Path
import shlex
import readline

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

PATH_COMMANDS = [key + " " for key in COMMANDS.keys()]



def get_path(cmd: str):
    paths = os.getenv('PATH').split(os.pathsep)
    for path in paths:
        cmd_path = os.path.join(path, cmd)
        if os.access(cmd_path, os.X_OK):
            return cmd_path
    return None

def build_path_commands():
    paths = os.getenv('PATH').split(os.pathsep)
    for path in paths:
        for _file in os.listdir(path):
            full_path = os.path.join(path, _file)
            if os.access(full_path, os.X_OK):
                PATH_COMMANDS.append(_file + " ")


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
        if mode != utils.RedirectTypes.NONE:
            output = args[-1]
            args = args[:index]
            _path = Path(output)
            _path.parent.mkdir(parents=True, exist_ok=True)
            _path.touch()

        if cmd in COMMANDS:
            fn = COMMANDS[cmd]
            try:
                result = fn(*args)
                if mode in (utils.RedirectTypes.STDIN, utils.RedirectTypes.STDIN_APPEND):
                    result += "\n"
                    utils.to_file(output, result, mode)
                else:
                    _print(result)
            except ShellException as e:
                if mode in (utils.RedirectTypes.STDERR, utils.RedirectTypes.STDERR_APPEND):
                    utils.to_file(output, result, mode)
                else:
                    _print(e)

        else:
            path = get_path(cmd)
            if path:
                res = subprocess.run([cmd, *args], capture_output=True, text=True)
                if mode in (utils.RedirectTypes.STDIN, utils.RedirectTypes.STDIN_APPEND):
                    utils.to_file(output, res.stdout, mode)
                else:
                    _print(res.stdout.rstrip())
                if res.stderr:
                    if mode in (utils.RedirectTypes.STDERR, utils.RedirectTypes.STDERR_APPEND):
                        utils.to_file(output,res.stderr, mode)
                    else:
                        sys.stdout.write(res.stderr)                    
            else:   
                sys.stdout.write(f"{cmd}: command not found \n")


def completer(text, state):
    options = [key for key in PATH_COMMANDS if key.startswith(text)]
    return options[state] if state < len(options) else None


if __name__ == "__main__":
    build_path_commands()
    readline.set_completer(completer)
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    main()

