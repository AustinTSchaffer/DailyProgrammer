import pytest

import app

@pytest.fixture
def solution() -> app.Solution:
    return app.Solution()

@pytest.fixture
def sample_gameboard_1():
    return [
        ['A','B','C','E'],
        ['S','F','C','S'],
        ['A','D','E','E'],
    ]

def test_board_1_contains_ABCCED(solution, sample_gameboard_1):
    assert solution.exist(sample_gameboard_1, "ABCCED")

def test_board_1_contains_SEE(solution, sample_gameboard_1):
    assert solution.exist(sample_gameboard_1, "SEE")

def test_board_1_not_contains_ABCB(solution, sample_gameboard_1):
    assert not solution.exist(sample_gameboard_1, "ABCB")

def test_board_1_no_diagonals(solution, sample_gameboard_1):
    assert not solution.exist(sample_gameboard_1, "AFE")

def test_null_condition(solution, sample_gameboard_1):
    assert solution.exist(sample_gameboard_1, "")

def test_spiral_pattern(solution, sample_gameboard_1):
    spiral = "ABCESEEDASFC"
    assert solution.exist(sample_gameboard_1, spiral)
    assert solution.exist(sample_gameboard_1, "".join(reversed(spiral)))

if __name__ == "__main__":
    pytest.main()
