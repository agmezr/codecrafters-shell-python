from enum import Enum
import subprocess
import select
import sys

class RedirectTypes(Enum):
    NONE=-1
    STDIN=1
    STDERR=2
    STDIN_APPEND=3
    STDERR_APPEND=4
    


def split_tokens(txt):
    result = []
    symbols = {
        "'": False,
    }
    txt = txt.replace("''", "")
    txt = txt.replace('""', "")
    special = ("'")
    word = []
    txt += " "
    for letter in txt:
        if letter in special:
            current = symbols[letter]
            if not current:
                symbols[letter] = True

            else:
                symbols[letter] = False
                result.append("".join(word))
                word.clear()
        elif letter == " ":
            current = symbols["'"]
            if not current:
                if word:
                    result.append("".join(word))
                    word.clear()
            else:
                word.append(letter)
        else:
            word.append(letter)
    return result


def find_redirect(args):
    for i, arg in enumerate(args):
        if arg in ("1>", ">"):
            return RedirectTypes.STDIN, i
        elif arg in ("2>"):
            return RedirectTypes.STDERR, i
        elif arg in ("1>>", ">>"):
            return RedirectTypes.STDIN_APPEND, i
        elif arg in ("2>>"):
            return RedirectTypes.STDERR_APPEND, i
    return RedirectTypes.NONE, -1

def to_file(path, content, rtype: RedirectTypes):
    mode = "a+" if rtype in (RedirectTypes.STDIN_APPEND, RedirectTypes.STDERR_APPEND) else "w+"
    with open(path, mode) as f:
        f.write(content)

def run_popen(cmd, args, file_path, mode):
    f = subprocess.Popen([cmd, *args],\
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,\
                          text=True)
    p = select.poll()
    p.register(f.stdout)

    if f.stderr:
        if mode in (RedirectTypes.STDERR, RedirectTypes.STDERR_APPEND):
                to_file(file_path , f.stderr.read(), mode)
        else:
            sys.stdout.write(f.stderr.read())
        return
    
    fm = "a+" if mode in (RedirectTypes.STDIN_APPEND, RedirectTypes.STDERR_APPEND) else "w+"
    _file = open(file_path, fm)
    while True:
        try:
            if p.poll(1):
                if file_path:
                    _file.write(f.stdout.readline())
                    _file.flush()
                else:
                    sys.stdout.write(f.stdout.readline())
        except KeyboardInterrupt:
            f.kill()
            _file.close()
            return