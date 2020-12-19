import os
import time

from ScriptUtilities import *


def getFilesWithExtension(directories: list, ext: str, recursive=False):
    for directory in directories:
        if not directory.is_dir():
            raise ValueError("Invalid directory path.")

    paths = []
    for directory in directories:
        if recursive:
            for folder in os.walk(directory):
                paths.extend([Path(folder[0]) / filename for filename in folder[2] if Path(filename).suffix == ext])
        else:
            (_, _, filenames) = next(os.walk(directory))
            paths.extend([Path(directory) / filename for filename in filenames if Path(filename).suffix == ext])

    return paths


def combineTextFiles(txt_paths: list, add_newline_to_end_of_each=False):
    lines = []
    for txt_path in txt_paths:
        new_lines = getTxtLines(txt_path)
        if add_newline_to_end_of_each:
            new_lines[-1] += "\n"
        lines.extend(new_lines)

    results_path = txt_paths[0].parent / time.strftime("combined_txt_files_%Y%M%d%H%m%S.txt")  # Results saved in first file's dir.
    with open(results_path, "w+", encoding="utf-8") as handle:
        for line in lines:
            handle.write(line)

    return results_path


def combineTextFilesInDirectories(txt_file_directories: list, recursive=False, add_newline_to_end_of_each=False):
    """
    Searches the given list of directories for .txt files, and combines them.
    """
    txt_paths = getFilesWithExtension(txt_file_directories, ".txt", recursive=recursive)
    return combineTextFiles(txt_paths, add_newline_to_end_of_each=add_newline_to_end_of_each)


if __name__ == "__main__":
    combineTextFilesInDirectories([Path(input("Enter path of directory in which to combine text files: "))],
                                  recursive=bool(int(input("Also search nested directories? (0/1) "))),
                                  add_newline_to_end_of_each=bool(int(input("Add newlines? (0/1) ")))
                                  )