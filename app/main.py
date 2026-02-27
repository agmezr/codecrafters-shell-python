import sys


def _echo(*args):
    txt = " ".join(args)
    sys.stdout.write(f"{txt}\n")


def _exit(*_):
    exit()


COMMANDS = {
    "echo": _echo,
    "exit": _exit
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
