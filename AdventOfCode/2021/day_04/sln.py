#%%
import common
import dataclasses
from typing import List

class BingoBoard:
    def __init__(self, data: str):
        self.data = [
            [
                value.strip()
                for value in row.split()
                if value.strip()
            ]
            for row in data.split('\n')
            if row
        ]

        self.marks = [[False for _ in __] for __ in self.data]

    def reset_marks(self):
        for row_index, row in enumerate(self.marks):
            for col_index, _ in enumerate(row):
                self.marks[row_index][col_index] = False

    def mark_number(self, number):
        for row_index, row in enumerate(self.data):
            for col_index, value in enumerate(row):
                if value == number:
                    self.marks[row_index][col_index] = True

    def is_complete(self) -> bool:
        columns = [True for _ in self.marks[0]]

        for row in self.marks:
            # Check row
            if all(row):
                return True

            # Check columns
            for col_index, value in enumerate(row):
                columns[col_index] = value and columns[col_index]

        return any(columns)

    def sum_unmarked(self) -> int:
        return sum(
            int(value)
            for row_index, row in enumerate(self.data)
            for col_index, value in enumerate(row)
            if not self.marks[row_index][col_index]
        )

bingo_numbers = common.get_input(__file__, filename='bingo_numbers.txt')[0].strip().split(',')
bingo_boards = list(map(BingoBoard, ''.join(common.get_input(__file__, filename='bingo_boards.txt')).split('\n\n')))

def run_bingo_simulation():
    for number in bingo_numbers:
        for bingo_board in bingo_boards:
            bingo_board.mark_number(number)
            if bingo_board.is_complete():
                print("Part 1:", int(number) * bingo_board.sum_unmarked())
                return

run_bingo_simulation()
for board in bingo_boards:
    board.reset_marks()

def run_bingo_simulation_part_2():
    bingo_boards_current = bingo_boards
    bingo_boards_next = list(bingo_boards)
    for number in bingo_numbers:
        for bingo_board in bingo_boards_current:
            bingo_board.mark_number(number)
            if bingo_board.is_complete():
                if len(bingo_boards_current) == 1:
                    print("Part 2:", int(number) * bingo_board.sum_unmarked())
                    return
                bingo_boards_next.remove(bingo_board)

        bingo_boards_current = bingo_boards_next
        bingo_boards_next = list(bingo_boards_current)

run_bingo_simulation_part_2()
for board in bingo_boards:
    board.reset_marks()

# %%


