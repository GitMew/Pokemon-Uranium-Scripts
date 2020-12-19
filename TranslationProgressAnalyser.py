import os

import WhitenImmediateDuplicateLines as Whiten
import CombineTextFiles as Combine
from ScriptUtilities import *


def countBlanks(lines: list):
    return lines.count("\n")


def countWords(lines: list):
    count = 0
    for line in lines:
        count += len(line.split(" "))
    return count


def getLinesSupersededByBlank(lines: list):
    return [lines[line_idx] for line_idx in range(len(lines) - 1) if lines[line_idx + 1] == "\n"]


def translationProgressAnalysis(actual_intl: Path, translated_intl: Path, mapstrikes: int=3):
    if not isValidTextFile(translated_intl):
        raise ValueError("Invalid text file.")

    intl_actual_copy = Whiten.whitenImmediateDuplicates(actual_intl)
    intl_trans_copy  = Whiten.whitenImmediateDuplicates(translated_intl)
    raw_lines        = getTxtLines(intl_actual_copy)
    translated_lines = getTxtLines(intl_trans_copy)

    data = {}
    data["full_linecount"] = countBlanks(raw_lines)
    data["full_wordcount"] = countWords(raw_lines) - countBlanks(raw_lines)

    data["untranslated_linecount"] = countBlanks(translated_lines)
    data["untranslated_wordcount"] = countWords(getLinesSupersededByBlank(translated_lines))

    data["translated_linecount"] = data["full_linecount"] - data["untranslated_linecount"]
    data["translated_wordcount"] = data["full_wordcount"] - data["untranslated_wordcount"]

    data["full_mapcount"] = 0
    for line in raw_lines:
        if "[Map" in line:
            data["full_mapcount"] += 1

    data["translated_mapcount"] = 0
    strikes = 0
    current_map = None
    exist_lines_untranslated = False
    for line in translated_lines:
        if "[Map" in line:
            if current_map is not None and not exist_lines_untranslated:
                data["translated_mapcount"] += 1
            current_map = line
            exist_lines_untranslated = False
        else:
            if line == "\n":
                if strikes < mapstrikes:
                    strikes += 1
                else:
                    exist_lines_untranslated = True

    os.remove(intl_actual_copy)
    os.remove(intl_trans_copy)

    return data


def pprintAnalysis(datadict: dict):
    print("===== Pokémon Uranium Translation Progress Analysis =====")
    print(" Translated words: {0}/{1} or {2}%"
          .format(datadict["translated_wordcount"],
                  datadict["full_wordcount"],
                  round(datadict["translated_wordcount"]/datadict["full_wordcount"] * 100, 2)))
    print(" Translated lines: {0}/{1} or {2}%"
          .format(datadict["translated_linecount"],
                  datadict["full_linecount"],
                  round(datadict["translated_linecount"]/datadict["full_linecount"] * 100, 2)))
    print(" Translated maps: {0}/{1} or {2}%"
          .format(datadict["translated_mapcount"],
                  datadict["full_mapcount"],
                  round(datadict["translated_mapcount"]/datadict["full_mapcount"] * 100, 2)))


if __name__ == "__main__":
    i = Combine.combineTextFilesInDirectories([
        Path("D:/Pokémon Uranium/public/workspace"),
        Path("D:/Pokémon Uranium/public/final"),
        Path("D:/Pokémon Uranium/public/review")])
    a = translationProgressAnalysis(Path("D:/Pokémon Uranium/public/_source/intl.txt"), i, mapstrikes=3)
    pprintAnalysis(a)

    import os
    os.remove(i)

# ToDo: Lots of testing ...