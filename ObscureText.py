"""
Text obscuring tool for Pokémon Uranium. The input is a text file containing regular language. The output is that same
text file, but with some characters, and sometimes entire words, "obscured" (replaced by a "-", for example) to imitate
having been burnt or faded.

Author: T. "Mew" B.
Date: 2020-07-30
Licence: CC-3.0 BY
"""
import numpy as np

from ScriptUtilities import *


def obscureWord(word: str, burn_char, word_burn_parameter, char_burn_parameter):
    """
    Obscures the given word partially or wholly using uniform probability distributions.
    :param word: The word to obscure
    :param burn_char: The character to obscure with
    :param word_burn_parameter: Parameter to determine whether each entire word will be burnt wholly by intention. Call this W,
                                then the probability of burn for word length L is exp(-L*(W-1.5)).
    :param char_burn_parameter: Probability that a character in an unburnt word will be burnt.
    :return: The partially or wholly obscured word.
    """
    rand = np.random.random()
    burnt_word = ""
    if rand < np.exp(-word_burn_parameter * (len(word) - 1.5) + np.log(1)):
        burnt_word += burn_char * len(word)
    else:
        for char in word:
            rand = np.random.random()
            if rand < char_burn_parameter:
                burnt_word += burn_char
            else:
                burnt_word += char

    return burnt_word


def obscureFile(text_file: Path, burn_char="-", word_burn_parameter=0.465, char_burn_parameter=0.25):
    """
    Obscures some letters and words in the given text file, and writes the results to a new file.
    :param text_file: The plaintext
    :param word_burn_parameter: Parameter to determine whether each entire word will be burnt wholly by intention. Call
                                this W, then the probability of burn for word length L is exp(-L*(W-1.5)). The default
                                value W=0.465 makes all 1-letter words get burnt, 80% of 2-letter words, 50% of 3,
                                33% of 4, 20% of 5, etc ...
    :param char_burn_parameter: Probability that a character in an unburnt word will be burnt.
    """
    if isValidTextFile(text_file):
        raise ValueError("Invalid text file.")
    lines = getTxtLines(text_file)

    with open(text_file.parent / (text_file.stem + "_obscured" + ".txt"), "w+", encoding="utf-8") as write_handle:
        burnt_lines = []
        for line in lines:
            burnt_line = []
            for word in line.strip().split(" "):
                burnt_line.append(obscureWord(word, burn_char, word_burn_parameter, char_burn_parameter))
            burnt_lines.append(" ".join(burnt_line))
        write_handle.write("\n".join(burnt_lines))


if __name__ == "__main__":
    obscureFile(Path("Enter file path of text file to obscure the lines of: "))