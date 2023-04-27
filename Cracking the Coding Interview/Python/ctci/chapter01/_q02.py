from collections import defaultdict
from typing import Dict


def check_permutation(string1: str, string2: str) -> bool:
    """
    Returns true if the 2 input strings contains the exact same characters,
    regardless of order. Uses `collections.defaultdict` to relate a string's
    characters to the number of times the character appears in the string.

    This algorithm has `O(n)` space and time complexity.
    """

    if len(string1) != len(string2):
        return False

    histogram1 = defaultdict(int)
    for character in string1:
        histogram1[character] += 1

    histogram2 = defaultdict(int)
    for character in string2:
        histogram2[character] += 1

    return _histograms_are_identical(histogram1, histogram2)


def check_permutation2(string1: str, string2: str) -> bool:
    """
    Returns true if the 2 input strings contains the exact same characters,
    regardless of order. This solution is identical to `check_permutation`
    except it does not use `collections.defaultdict`.

    This algorithm has `O(n)` space and time complexity.
    """

    if len(string1) != len(string2):
        return False

    histogram1 = {}
    for c in string1:
        histogram1[c] = 1 + histogram1.setdefault(c, 0)

    histogram2 = {}
    for c in string2:
        histogram2[c] = 1 + histogram2.setdefault(c, 0)

    return _histograms_are_identical(histogram1, histogram2)


def _histograms_are_identical(histogram1: dict, histogram2: dict) -> bool:
    """
    Returns true if the 2 histograms are the same, meaning they have the same
    set of keys, which all point to the same values.

    In Python, this can be simplified to `histogram1 == histogram2`, but that
    defeats the purpose of this exercise. Production code should just use `==`.
    """

    if len(histogram1) != len(histogram2):
        return False

    for key, num_occurrece in histogram1.items():
        if key not in histogram2 or histogram2[key] != num_occurrece:
            return False

    return True
