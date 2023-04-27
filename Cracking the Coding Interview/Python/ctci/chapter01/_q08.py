from typing import List


def zero_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Sets entire rows and columns of the input matrix to 0 if any
    of the values in the row or column are 0.

    Modifies and returns the input matrix.
    """

    cols_to_0 = set()
    rows_to_0 = set()
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == 0:
                rows_to_0.add(i)
                cols_to_0.add(j)

    for i, row in enumerate(matrix):
        for j, _ in enumerate(row):
            if (i in rows_to_0) or (j in cols_to_0):
                matrix[i][j] = 0

    return matrix
