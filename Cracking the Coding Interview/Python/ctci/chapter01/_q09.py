import functools


def is_rotation(s1: str, s2: str) -> bool:
    """
    Returns True if s1 and s2 are rotations of each other.

    If s1 and s2 are rotations of each other, they are the same length and the
    concatenation of one of the strings to itself will contain the other.

    """

    if len(s1) != len(s2):
        return False

    return s1 in (s2 * 2)
