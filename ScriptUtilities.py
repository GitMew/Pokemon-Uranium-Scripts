from pathlib import Path


def isValidTextFile(path: Path):
    return path.is_file() and path.suffix == ".txt"


def validateIntl(path: Path):
    """
    Verifies whether the given path points to an existing file, and that said file is a txt or csv. Returns a valid path
    to a .txt Intl file if so.
    """
    if not path.is_file() or path.suffix not in [".txt", ".csv"]:
        raise ValueError("Invalid intl file provided.")

    if path.suffix == ".txt":
        return path
    elif path.suffix == ".csv":
        return csvIntlToTxtIntl(path)


def peekline(reading_filehandle):
    """
    Non-advancing alternative to readline().
    """
    t = reading_filehandle.tell()
    line = reading_filehandle.readline()
    reading_filehandle.seek(t)
    return line


def peeklines(reading_filehandle, line_amount=5):
    t = reading_filehandle.tell()
    lines = []
    for line_idx in range(line_amount):
        lines.append(reading_filehandle.readline())
    reading_filehandle.seek(t)
    return lines


def getTxtEncoding(path: Path):
    import chardet
    with open(path, "rb") as bytehandle:
        return chardet.detect(
            b"".join(peeklines(bytehandle, line_amount=20))  # At 3, 5, 10 ... lines, I got erroneous detections of "ascii".
        )["encoding"]  # Usually "utf-8-sig".


def getTxtLines(path: Path, encoding=None):
    with open(path, "r+", encoding=(getTxtEncoding(path) if encoding is None else encoding)) as handle:
        return handle.readlines()  # This does close the file.


def csvIntlToTxtIntl(path: Path):
    import csv

    with open(path, "r+", encoding="utf-8-sig", newline='') as read_handle:
        cursor = csv.DictReader(read_handle, delimiter=',', quotechar='\"')

        headers = cursor.fieldnames
        try:
            en_key = headers[headers.index("en")]
            langs = [name for name in headers if len(name) == 2 and not name == "en"]
            lang_key = langs[0]
        except:
            raise KeyError("No two-letter language indicator found for English or other language in header.")

        results_path = path.parent / (path.stem + ".txt")
        with open(results_path, "w+", encoding="utf-8") as write_handle:
            write_handle.write("[{0}]\n".format(path.stem))
            for row in cursor:
                write_handle.write(row[en_key] + "\n")
                write_handle.write(row[lang_key] + "\n")
    return results_path


def linesToTxt(lines: list, output_path: Path, add_newlines=True):
    with open(output_path, "w+", encoding="utf-8") as handle:
        handle.write(("\n" if add_newlines else "").join([str(line) for line in lines]))


if __name__ == "__main__":
    csvIntlToTxtIntl(Path("data/fr97.csv"))