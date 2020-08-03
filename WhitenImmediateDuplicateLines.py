from pathlib import Path
import os


def isValidIntl(path_intl: Path):
    return path_intl.is_file() and path_intl.suffix == ".txt"


def whitenImmediateDuplicates(intl: Path, line_amount: int=-1):
    if not isValidIntl(intl):
        raise ValueError("Invalid Intl file.")

    with open(intl, "r+", encoding="utf-8-sig") as handle:
        lines = handle.readlines()

    with open(intl.parent / (intl.stem + "_whitened" + ".txt"), "w+", encoding="utf-8") as handle:
        i = 0
        count = 0
        while i < len(lines) - 1:
            if (count < line_amount or line_amount < 0) and (lines[i] == lines[i+1] or lines[i] == lines[i+1] + "\n"):
                lines[i+1] = "\n"
                count += 1
            handle.write(lines[i])
            i += 1
        handle.write(lines[-1] if not lines[-1].endswith("\n") else lines[-1][:-1])


def batchProcessFolder(folder: Path, line_amount: int=-1):
    (_, _, filenames) = next(os.walk(folder))
    for filename in filenames:
        path = folder / filename
        if isValidIntl(path):
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
