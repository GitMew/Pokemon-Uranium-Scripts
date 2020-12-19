import itertools
import numpy as np

from ScriptUtilities import *


### Dumb functions (split into N parts and split into parts of N lines)
def splitIntoNParts(txt_file: Path, part_amount: int):
    if not isValidTextFile(txt_file):
        raise ValueError("Invalid text file.")

    lines = getTxtLines(txt_file)

    for i in range(1 + (len(lines) - 1) // part_amount):
        with open(txt_file.parent / (txt_file.stem + "_part_{0}".format(i) + ".txt"), "w+", encoding="utf-8") as handle:
            handle.write(lines[part_amount*i:part_amount*(i+1)])


def splitIntoPartsOfNLines(txt_file: Path, line_amount: int):
    if not isValidTextFile(txt_file):
        raise ValueError("Invalid text file.")

    lines = getTxtLines(txt_file)

    for i in range(1 + (len(lines) - 1) // line_amount):
        with open(txt_file.parent / (txt_file.stem + "_part_{0}".format(i) + ".txt"), "w+", encoding="utf-8") as handle:
            handle.write(lines[line_amount*i:line_amount*(i+1)])


def splitAtSymbol(txt_file: Path, symbol, encoding=None):
    raw_lines = getTxtLines(txt_file, encoding=encoding)

    parts = [[]]
    current_part_idx = 0
    for line in raw_lines:
        if symbol in line and len(parts[0]):
            parts.append([])
            current_part_idx += 1
        parts[current_part_idx].append(line)

    for part_idx in range(len(parts)):
        linesToTxt(parts[part_idx], txt_file.parent / "{0}_part_{1}.txt"
                   .format(txt_file.stem, part_idx), add_newlines=False)


### Smart functions (split based on an indicator and a target occurrence amount, by optimising
def smartTextFileSplitterOnSymbol(txt_file: Path, symbol: str, occurrence_target: int, occurence_max: int, splitting_stem: str):
    """
    Splits the given text file into parts delimited by the given symbol. The parts will roughly be of equal size, aiming
    for the given hint how many of the given symbol occurs in each part.
    """
    with open(txt_file, "r+", "utf-8-sig") as handle:
        lines = handle.readlines()

    mask = [1 if symbol in line else 0 for line in lines]
    parts = smartListMerger(
        splitListAtOccurences(mask, element=1),
        element=1,
        target_occurrences=occurrence_target,
        maximum_occurrences=occurence_max
    )

    if parts is None:
        print("No suitable splitting conditions found.")
        return

    current_line = 0
    occurrences = 0
    for part_mask in parts:
        with open(txt_file.parent / "{0}_{1}-{2}.txt".format(splitting_stem, occurrences, occurrences+part_mask.count(1))) as handle:
            handle.write(lines[current_line:current_line+len(part_mask)])

        occurrences += part_mask.count(1)
        current_line += len(part_mask)
    print("Smart split complete.")  # Maybe some analytics here, like a fitness score.
    return


def smartListMerger(parts: set,
                    element, target_occurrences: int, maximum_occurrences: int,
                    memo=list()):  # With 206 Maps, there are 5 * 10^61 possible configurations (sum_{n=0}^205 nCr(205, n)).
    """
    Backtracking algorithm for merging the lists in a given list such that, in the end, each resulting list contains
    approximately a target_occurrences amount of the given element (and certainly not more than maximum_occurences).
    """
    # Run through possible merges (one possible merge happens per iteration, disjunctly)
    possible_mergecodes = itertools.combinations(range(0,len(parts)), 2)
    solutions = []
    for code in possible_mergecodes:
        # Excluded cases:
        new_parts = parts[0:code[0]] + parts[code[0]+1:code[1]] + parts[code[1]+1:] + [parts[code[0]] + parts[code[1]]]
        # ToDo: This is concatenation-order dependent. To solve this, the parts list should be a set. Sadly, parts are
        #       lists, and a set can't contain a list. Solution: use tuples for the parts. Those are hashable.
        #
        #
        if new_parts in memo:
            continue

        merged_occ_max = max([part.count(element) for part in parts])
        if merged_occ_max > maximum_occurrences:
            continue

        # Base case:
        memo.add(new_parts)
        solutions.append(new_parts)

        # Recursive case:
        solution = smartListMerger(
            new_parts,
            element,
            target_occurrences,
            maximum_occurrences
        )
        if solution is not None:
            solutions.append(solution)

    return getMinimalErrorSolution(solutions, element, target_occurrences, 0.5, 0.5)  # ToDo: 50-50 is probably bad. Also, is std normalised?


def getMinimalErrorSolution(solutions: list,
                            element, target_occurences, occurrence_score_weight, line_score_weight):
    minimal_solution = None
    minimal_score = float("inf")

    for solution in solutions:
        score = calculateErrorScore(solution, element, target_occurences, occurrence_score_weight, line_score_weight)
        if score < minimal_score:
            minimal_score = score
            minimal_solution = solution

    return minimal_solution


def calculateErrorScore(parts,
                        element, target_occurences, occurence_score_weight, line_score_weight):
    # Score is calculated based on:
    #   1. How close does each list in the "parts" collection stay to the target occurences of the element? (Could be a standard deviation from the "supposed mean".)
    #   2. How closely tied are the lengths of each list? (Could be calculated via standard deviation; that way, normalsation is easier.)
    occs = [part.count(element) for part in parts]
    rel_standdev_occs = np.sqrt(sum([(occ - target_occurences) ** 2 for occ in occs]) / (len(parts) - 1))
    occurence_score = rel_standdev_occs

    linecounts = [len(part) for part in parts]
    standdev_linecounts = np.std(linecounts)
    line_score = standdev_linecounts

    return occurence_score*occurence_score_weight + line_score*line_score_weight


def splitListAtOccurences(lst, element):
    parts = []
    latest_idx = 0
    while latest_idx < len(lst):
        try:
            parts.append(lst[latest_idx:lst.index(element, latest_idx+1)])
            latest_idx = lst.index(element, latest_idx+1)
        except:
            parts.append(lst[latest_idx:])
    return parts


if __name__ == "__main__":
    splitAtSymbol(Path(input("Enter path of file to be split: ")), input("Text to split on: "), "utf-8")
    #smartTextFileSplitterOnSymbol("data/intl.txt", "[Map", 2, 8, "Intl")