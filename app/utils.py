from enum import Enum


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
    mode = "a+" if rtype.name == RedirectTypes.STDIN_APPEND.name else "w+"
    with open(path, mode) as f:
        f.write(content)
