import array
import queue
import urllib
from typing import List, Iterable


def urlify(some_string: str) -> str:
    """

    Replaces all spaces in the input string with "%20". Trivial solution. Uses
    the built-in `str.replace`.

    """
    return str.replace(some_string, " ", r"%20")


def inplace_urlify(character_array: array.array) -> array.array:
    """

    Replaces all spaces in the input array with `"%20"`. Requires that the
    array's `typecode` is set to `'u'` and that the array that is long enough to
    hold all of the characters that will be added, which will be equal to the
    length of the input string, plus 2 additional characters for every space
    that appears in the string. The buffer characters at the end of the array
    can be any value.

    This allows the method to perform an in-place string replacement, kinda. It
    uses a queue in order to keep track of the characters that need to be added,
    in the order that they need to be added, then loops through the array. If the
    current position of the array is NOT a space, it is added to the end of the
    queue. If the current position of the array IS a space, the characters `%`,
    `2`, and `0` are appended to the end of the queue. Then, the current position
    of the character array is replaced with the character from the front of the
    queue.

    The space complexity of this algorithm will be no less than 3 times the
    number of spaces in the input array, and will certainly be larger due to the
    overhead of maintaining a Python character queue.

    """

    assert character_array.typecode == "u"

    deferred_characters = queue.Queue()

    i = 0
    while i < len(character_array):
        if character_array[i] == " ":
            deferred_characters.put("%")
            deferred_characters.put("2")
            deferred_characters.put("0")
        else:
            deferred_characters.put(character_array[i])

        character_array[i] = deferred_characters.get()
        i += 1

    return character_array


def true_urlify(some_string: str) -> str:
    """
    Uses `urllib.parse.quote`, which catches more than just spaces.
    """

    return urllib.parse.quote(some_string)
