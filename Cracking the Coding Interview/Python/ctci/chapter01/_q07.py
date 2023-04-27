from typing import List, Any


def rotate_matrix(matrix: List[List[Any]], in_place=True) -> List[List[Any]]:
    """
    Rotates an NxN matrix by 90 degrees, clockwise. Creates a new matrix by
    default. If `in_place` is set True, the rotation is applied to the input
    matrix. Otherwise, a new NxN matrix is returned.
    """

    height = len(matrix)
    for row in matrix:
        assert len(row) == height, "The input matrix is not a square"

    _matrix = matrix if in_place else [[element for element in row] for row in matrix]

    return _rotate(_matrix)


def _rotate(matrix: List[List[Any]]) -> List[List[Any]]:
    """
    Rotates the input matrix by 90 degrees, clockwise.
    """

    n = len(matrix)

    # Calculates the number of "shells" in the matrix, where the outermost "shell"
    # is comprised of all of the elements in the matrix that border the matrix's
    # perimiter. The next shell would be all of the elements that meet the same
    # criteria as the first shell, if the first shell is completely removed from
    # the matrix. The matrix will then be rotated in-place, one shell at a time.
    #
    # For square matrices that have an even side length, `shell_count` will be half
    # of the side length. As an example, `n==4` results in a shell count of 2. For
    # square matrices that have an odd side length, `shell_count` will be `n-1/2`,
    # since the rotation of the very center shell will be identical, since it is
    # comprised by a single entity.

    shell_count = int(n / 2.0)
    for shell in range(shell_count):

        # Iterate for every element in the top row for each shell, except for
        # the last. This element should be referred to as the "primary"
        # element, which defines a group of 4 elements that will be rotated
        # within the current shell. Each element in this group will have their
        # values rotates one position in the clockwise direction.
        for primary in range(shell, n - shell - 1):

            # Store the current value of the primary element, since its value
            # has to make a round trip all the way around the shell.
            temp = matrix[shell][primary]

            # Rotates all of the elements in the group using the following
            # calculations, which determine the indexes of the elements that
            # are in the current group, within the current shell.

            # `x` is the row index of the element that is 90 degrees
            # counterclockwise from the current primary value.

            x = n - primary - 1

            # `y` is the column index of the element that is 90 degrees clockwise
            # from the current primary value. This value can be calculated once
            # per loop, but the description of its value is more easily explained at
            # this point in the code.

            y = n - shell - 1

            # This section is what dictates whether the rotation is clockwise
            # or counter clockwise. This section could also be repurposed to
            # rotate the matrix 180 degrees.

            matrix[shell][primary] = matrix[x][shell]
            matrix[x][shell] = matrix[y][x]
            matrix[y][x] = matrix[primary][y]
            matrix[primary][y] = temp

    # Returns the matrix input matrix, after having rotated its values.

    return matrix


def print_matrix(matrix: List[List[Any]]):
    """
    Prints an input matrix, attempting to keep column alignment.
    """

    padding = max(
        len(str(value))
        for value in row
        for row in matrix
    )

    for row in matrix:
        for value in row:
            print(str(value).ljust(padding, " "),  end = " ")
        print ("")
