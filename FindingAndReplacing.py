import time
import os

from ScriptUtilities import *
import CombineTextFiles as Comb

def countWord(text_file: Path, word: str):
    """
    Counts how many times the given word appears in the text file.
    """
    lines = getTxtLines(text_file)
    count = 0
    for line in lines:
        count += line.count(word)
    return count


def wordCount(text_file: Path, word: str):
    """
    Counts how many words the text file contains.
    """
    lines = getTxtLines(text_file)
    count = 0
    for line in lines:
        count += len(line.split(" "))
    return count


def findWordLinenos(text_file: Path, word: str, do_save_duplicates=False):
    """
    Returns the line numbers of each occurence of the given word in the text file. Duplicate line numbers
    can be disabled.
    """
    lines = getTxtLines(text_file)#, encoding="utf-8-sig")
    idcs = []
    for line_idx in range(len(lines)):
        count = lines[line_idx].count(word)
        if count:
            if do_save_duplicates:
                idcs.extend([line_idx+1] * count)
            else:
                idcs.append(line_idx+1)  # Notice we're using 1-based indexing in the output; see, e.g., NP++.
    return idcs


def findWordLinenosToTxt(p: Path, w: str, do_save_duplicates=False):
    f = findWordLinenos(p, w, do_save_duplicates=do_save_duplicates)
    linesToTxt(["Total line count: {0}".format(len(f))] + ["Word found: {0}\n".format(w)] + f,
        p.parent / (p.stem + "_find_" + time.strftime("%Y%M%d%H%m%S") + ".txt")
    )


def findWordLinenos_Dir(dir: Path, w: str, file_ext: str, do_save_duplicates=False):
    linenos = []
    files = Comb.getFilesWithExtension([dir], ext=file_ext, recursive=False)

    for file in files:
        linenos.append("\n{0}".format(file.name))
        linenos.extend(
            findWordLinenos(file, w, do_save_duplicates=do_save_duplicates)
        )
    linesToTxt(
        ["Total occurences found: {0}".format(len(linenos) - len(files))] + ["Word found: {0}\n".format(w)] + linenos,
        dir / (dir.stem + "_find_" + time.strftime("%Y%M%d%H%m%S") + ".txt")
    )


def findLatex(txt: Path, command: str, parentheses: list, do_crash_on_mismatch=False):
    lines = getTxtLines(txt, encoding="utf-8")
    all_text = "".join([line.strip() for line in lines])

    start_command = command + parentheses[0]
    start_p = parentheses[0]
    end_p   = parentheses[1]

    found = []
    stack = []  # Element format: (pattern, index)

    idx = 0
    while idx < len(all_text):
        try:
            c = all_text.index(start_command, idx)
        except:
            c = float("inf")

        try:
            s = all_text.index(start_p, idx)
        except:
            s = float("inf")

        try:
            e = all_text.index(end_p, idx)
        except:
            e = float("inf")

        closest_idx = min(c,s,e)
        if closest_idx == -1:
            print("Successfully covered all points of interest.")
            break

        elif closest_idx == c:
            stack.append((start_command, closest_idx))
            idx = closest_idx + len(start_command)

        elif closest_idx == s:
            stack.append((start_p, closest_idx))
            idx = closest_idx + len(start_p)

        elif closest_idx == e:
            try:
                current_activity = stack.pop()
            except:
                if do_crash_on_mismatch:
                    print("Terminated early: closing parenthesis without opening parenthesis.")
                    break

            if current_activity[0] == start_command:
                found.append(
                    all_text[current_activity[1]:closest_idx+len(end_p)]
                )
            idx = closest_idx + len(end_p)

        if do_crash_on_mismatch and len(stack):
            print("Terminated at end: opening statements without closing parenthesis: {0}".format(stack))

    return found


def findLatexToTxt(p, c, parens):
    content = findLatex(p, c, parens)

    linesToTxt(["Total count: {0}".format(len(content))] + ["Command looked for: {0}\n".format(c + "".join(parens))] + content,
        p.parent / (p.stem + "_findcommand_" + time.strftime("%Y%M%d%H%m%S") + ".txt")
    )


if __name__ == "__main__":
    #findWordLinenosToTxt(
    #   Path(input("Enter path of file to search word in: ")),
    #   input("Word to find: "),
    #   bool(int(input("Save duplicates? (0/1) ")))
    # )
    # findLatexToTxt(Path(input("Enter path of file to search parentheses in: ")),
    #           input("Command (left parenthesis prefix): "),
    #           [input("Left parenthesis: "), input("Right parenthesis: ")])
    findWordLinenos_Dir(Path(input("Enter path of directory to search word in: ")),
                        input("Word to find: "),
                        input("File extension: "),
                        bool(int(input("Save duplicates? (0/1) ")))
                        )