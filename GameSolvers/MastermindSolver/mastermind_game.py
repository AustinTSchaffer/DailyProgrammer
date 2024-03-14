import collections
import dataclasses
import secrets
from typing import Tuple

@dataclasses.dataclass(frozen=True)
class Result:
    right_color_right_spot: int
    right_color_wrong_spot: int

class MastermindCoreMechanic:
    def __init__(self, colors: int, slots: int):
        self.colors = colors
        self.slots = slots

        # That feeling when you use Python's cryptographically secure
        # random number generator, but plan on running the guessing agent
        # in the same Python runtime environment via Arbitrary Code Execution.
        # Better use an underscore to make sure the code is safely hidden! /s
        self._code = tuple(secrets.randbelow(colors) for i in range(slots))

    def interpret_guess(self, guess: Tuple[int]) -> Tuple[int]:
        if len(guess) != self.slots:
            raise ValueError(f"guess was not the correct length (expected {self.slots}, actual {len(guess)})")
        
        colors_out_of_range = {
            color for color in guess
            if (not isinstance(color, int)) or (color >= self.colors) or (color < 0)
        }

        if colors_out_of_range:
            raise ValueError(f"Colors must be integers between 0 and {self.colors-1}. Colors not in range: {colors_out_of_range}")

        right_color_right_spot = 0
        right_color_wrong_spot = 0

        unmatched_code_bits = collections.defaultdict(int)
        unmatched_guess_bits = collections.defaultdict(int)
        for code_bit, guess_bit in zip(self._code, guess):

            # If the current guess bit exactly matches the current code bit...
            if code_bit == guess_bit:
                right_color_right_spot += 1

                # Personal preference, I prefer using a continue as opposed to an
                # else that changes the indentation of everything after this.
                continue

            # If the guess bit matches a previously seen code bit...
            if unmatched_code_bits[guess_bit] > 0:
                right_color_wrong_spot += 1
                # Replace the previously seen code bit with the current code bit
                unmatched_code_bits[guess_bit] -= 1
                unmatched_code_bits[code_bit] += 1
            else:
                unmatched_guess_bits[guess_bit] += 1

            # If the code bit matches a previously seen guess bit...
            if unmatched_guess_bits[code_bit] > 0:
                right_color_wrong_spot += 1
                # Replace the previously seen guess bit with the current code bit
                unmatched_guess_bits[code_bit] -= 1
                unmatched_guess_bits[guess_bit] += 1
            else:
                unmatched_code_bits[code_bit] += 1
        
        return Result(right_color_right_spot, right_color_wrong_spot)
