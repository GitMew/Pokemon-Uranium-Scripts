import CombineTextFiles as Combine
from ScriptUtilities import *


def whitenImmediateDuplicates(intl: Path, line_amount: int=-1):
    if not isValidTextFile(intl):
        raise ValueError("Invalid Intl file.")

    lines = getTxtLines(intl)

    results_file = intl.parent / (intl.stem + "_whitened" + ".txt")
    with open(results_file, "w+", encoding="utf-8") as handle:
        i = 0
        count = 0
        while i < len(lines) - 1:
            if (count < line_amount or line_amount < 0) and (lines[i] == lines[i+1] or lines[i] == lines[i+1] + "\n"):
                lines[i+1] = "\n"
                count += 1
            handle.write(lines[i])
            i += 1
        handle.write(lines[-1] if not lines[-1].endswith("\n") else lines[-1][:-1])

    return results_file


def batchProcessFolder(folder: Path, line_amount: int=-1):
    if not folder.is_dir():
        raise ValueError("Invalid directory path.")

    paths = Combine.getFilesWithExtension([folder], ".txt", recursive=False)
    for path in paths:
        whitenImmediateDuplicates(path, line_amount)


if __name__ == "__main__":
    mode = ""
    while mode != "s" and mode != "b":
        mode = input("Single or batch process? (s/b) ").lower()

    if mode == "s":
        target = Path(input("Enter path of Intl file: "))
        amnt = int(input("Amount of duplicates to whiten (negative number means \"all\"): "))
        whitenImmediateDuplicates(target, amnt)
    elif mode == "b":
        target = Path(input("Enter path Intl folder to be batch-processed: "))
        amnt = int(input("Amount of duplicates to whiten per file (negative number means \"all\"): "))
        batchProcessFolder(target, amnt)
