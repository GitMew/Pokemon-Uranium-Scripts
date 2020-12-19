import os
import time
from pathlib import Path


def createFolderPerFilename(directory: Path, do_extension=False):
    """
    Creates a folder for each file in the given directory, in that directory, with the same name as the file.
    """
    if not directory.is_dir():
        raise ValueError("Invalid directory.")

    (_, _, filenames) = next(os.walk(directory))
    new_folder_paths = []

    for filename in filenames:
        f = Path(filename)
        new_path = directory / (f.stem if not do_extension else f.stem + f.suffix[1:])
        try:
            new_path.mkdir(exist_ok=False, parents=True)
            new_folder_paths.append(new_path)
        except:  # Due to exist_ok=False, this is how we detect that we shouldn't add the path to the new list.
            pass

    return new_folder_paths


def refactorFilenames(directory: Path, old: str, new: str, do_folders=False):
    (_, folders, filenames) = next(os.walk(directory))

    for filename in filenames:
        (directory / filename).rename(directory / (filename.stem.replace(old, new) + filename.suffix))

    if do_folders:
        for folder in folders:
            (directory / folder).rename(directory / folder.replace(old, new))


def flattenFolderContents(folder: Path):
    # Collect all files
    file_paths = []
    for subfolder in os.walk(folder):
        sub = Path(subfolder[0])
        for filename in subfolder[2]:
            file_paths.append(sub / filename)

    # Find duplicate filenames
    filenames = [path.name for path in file_paths]
    duplicate_names = set()
    for filename in filenames:
        if filenames.count(filename) != 1:
            duplicate_names.add(filename)

    # Move all files that're not duplicates
    for file_path in file_paths:
        if filenames.count(file_path.name) != 1:
            continue
        file_path.rename(folder / file_path.name)


def filenamesToTxt(directory: Path):
    (_, folders, filenames) = next(os.walk(directory))

    with open(directory / time.strftime("directory_contents_%Y%M%d-%H%m%S.txt"), "a+") as handle:
        for folder in folders:
            handle.write(folder + "\n")
        for file in filenames:
            handle.write(file + "\n")


if __name__ == "__main__":
    createFolderPerFilename(Path(input("Enter folder path to create subfolders per file for: ")),
                             do_extension=bool(int(input("Keep extension in folder names? (0/1) "))))
    #
    # refactorFilenames(Path(input("Enter folder path to rename files in: ")),
    #                   old=input("Text to replace: "),
    #                   new=input("Text to replace by: "),
    #                   do_folders=bool(int(input("Rename folders as well? (0/1)"))))
    #
    # flattenFolderContents(Path(input("Enter folder to flatten: ")))
    # filenamesToTxt(Path(input("Enter directory to map out: ")))