import collections
import math

from typing import Optional


class Operation(object):
    """
    Defines a single-character operation against a string.

    - operation: "insert", "remove", "change", or "nothing"
    - index: the index where a change should be made to a string (0-based index)
        - if "insert", insert at index
        - if "remove", remove character at index
        - if "change", change character at index
        - if "nothing", index will be None
    - character: the character that will be changed, added, removed, or None if "nothing"
    """

    def __init__(self, operation: str, index: int, character: str):
        self.operation = operation
        self.index = index
        self.character = character

    def apply(self, some_string: str) -> str:
        """
        Applies this operation to `some_string`.
        """

        assert self is not None

        if self.operation is None:
            return some_string

        operation = self.operation.strip().lower()

        if operation == "nothing":
            return some_string

        if operation == "remove":
            return some_string[: self.index] + some_string[self.index + 1 :]

        if operation == "change":
            return (
                some_string[: self.index]
                + self.character
                + some_string[self.index + 1 :]
            )

        if operation == "insert":
            return (
                some_string[: self.index] + self.character + some_string[self.index :]
            )

        assert False, "Unrecognized operation: {}".format(operation)


def one_away(s1: str, s2: str) -> Optional[Operation]:
    """
    Returns an Operation, which describes an operation and an index that can be used to
    convert one string1 into string2, if it is possible. Returns None otherwise.
    The possible operations are:

    - insert 1 character
    - remove 1 character
    - change 1 character
    - do nothing

    """

    # Cache the str lengths up front, just in case `len(str)` is an `O(n)`
    # operation, also because it's easier to type and read the variables. These
    # variables can be replaced with the source function call throughout this
    # function, if needed.

    len_s1 = len(s1)
    len_s2 = len(s2)
    len_shorter_string = min(len_s1, len_s2)
    len_longer_string = max(len_s1, len_s2)

    if len_longer_string - len_shorter_string > 1:
        # If the strings have a difference in length that is more than 1,
        # then they are more than 1 character different.
        return None

    head_length = 0
    while head_length < len_shorter_string:
        if s1[head_length] != s2[head_length]:
            break
        head_length += 1

    # `head_length` is now equal to the number of characters
    # that match between the 2 strings at the head of each string.

    if head_length == len_s1 and head_length == len_s2:
        # If `head_length` is the same length as both of the strings,
        # then the strings are the same.
        return Operation("nothing", None, None)

    # Perform a similar operation to get the matching tail length, except
    # with a few optimizations to keep the tail from searching the same
    # span as the head length.

    tail_length = 0
    while tail_length < (len_shorter_string - head_length):
        if s1[-(tail_length + 1)] != s2[-(tail_length + 1)]:
            break
        tail_length += 1

    # `tail_length` is now equal to the number of characters
    # that match between the 2 strings at the tail of each string.

    if head_length + tail_length + 1 < len_longer_string:
        # This test checks to see if there are more than 1 characters sandwiched
        # between indicating that there are 2 or more characters that do not match.
        return None

    if len_s1 == len_s2:
        # This indicates that the operation is "change", which transforms
        # s1 to s2 by changing the `head_length`th character of s1 to
        # the `head_length`th character of s2 (using 0-based indexes)
        return Operation("change", head_length, s2[head_length])

    if len_s1 > len_s2:
        # This indicates that the operation is "remove", which transforms
        # s1 to s2 by removing the `head_length`th character of s1 (using
        # 0-based indexes)
        return Operation("remove", head_length, s1[head_length])

    # This final remaining case indicates that the operation is "insert", which
    # transforms s1 to s2 by inserting the `head_length`th character of s2 into
    # s1, at the `head_length`th index (again, using 0-based indexes).
    return Operation("insert", head_length, s2[head_length])


def is_one_away(string1: str, string2: str) -> bool:
    """
    Returns true if applying `one_away` to string1 and string2 is not `None`.
    """

    return one_away(string1, string2) is not None
