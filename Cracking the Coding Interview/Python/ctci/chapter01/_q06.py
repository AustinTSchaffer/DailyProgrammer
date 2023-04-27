def compress(some_string: str) -> str:
    """

    Compresses `some_string` using a naive compression algorithm, which converts
    continuous runs of characters to
    `"{}{}".format(character, number_of_continuous_appearances)`

    The flaw with this approach is that it is impossible to correctly decompress
    a string in cases where the original string contained numbers. As an
    example, `aab2cc` compresses to `a2b121c2`, which would indicate to the
    decompression algorithm that `b` needs to be repeated 121 times.

    """

    if len(some_string) <= 0:
        return some_string

    output = [[some_string[0], 1]]
    length_so_far = 0

    for char in some_string[1:]:
        if output[-1][0] == char:
            output[-1][1] += 1
        else:
            length_so_far += 1 + len(str(output[-1][1]))
            if length_so_far > len(some_string):
                return some_string
            output.append([char, 1])

    length_so_far += 1 + len(str(output[-1][1]))
    if length_so_far > len(some_string):
        return some_string

    return "".join(map(lambda tup: tup[0] + str(tup[1]), output))
