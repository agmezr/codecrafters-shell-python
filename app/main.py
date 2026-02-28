import sys
import os

def _print(s):
    sys.stdout.write(f"{s}\n")

def _echo(*args):
    txt = " ".join(args)
    sys.stdout.write(f"{txt}\n")


def _exit(*_):
    exit()

def _type(*args):
    t = args[0]
    if t in COMMANDS:
        _print(f"{t} is a shell builtin")
    else:
        if not verify_command(t):
            _print(f"{t}: not found")



COMMANDS = {
    "echo": _echo,
    "exit": _exit,
    "type": _type
}

def verify_command(cmd: str):
    paths = os.getenv('PATH').split(os.pathsep)
    for path in paths:
        cmd_path = os.path.join(path, cmd)
        if os.access(cmd_path, os.X_OK):
            _print(f"{cmd} is {cmd_path}")
            return True

    return False


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
            sys.stdout.write(f"{cmd}: command not found \n")
    

if __name__ == "__main__":
    main()
