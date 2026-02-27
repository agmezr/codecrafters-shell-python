import sys


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
        _print(f"{t}: not found")



COMMANDS = {
    "echo": _echo,
    "exit": _exit,
    "type": _type
}

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
