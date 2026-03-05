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
            return 1, i
    return -1, -1

def to_file(path, content):
    with open(path, "w+") as f:
        f.write(content)
