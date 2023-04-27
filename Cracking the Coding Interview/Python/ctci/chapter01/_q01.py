def isunique(some_str: str) -> bool:
    """
    Returns true if the input string contains only unique characters. Uses a
    `set` to keep track of the characters it has already seen in some_str.

    This algorithm has `O(n)` space complexity and `O(n)` time complexity.
    """

    previously_seen_characters = set()

    for char in some_str:
        if char in previously_seen_characters:
            return False
        previously_seen_characters.add(char)

    return True


def isunique2(some_str: str) -> bool:
    """
    Returns true if the input string contains only unique characters, without
    using any additional data structures. This is accomplished by checking each
    character in the input string against all of the characters that preceeded it.

    This algorithm has constant space complexity, but `O(n^2)` time complexity.
    """
    for index, char in enumerate(some_str):

        # Use a slice to check the current character against all preceeding
        # characters.

        if char in some_str[0:index]:
            return False

    return True

