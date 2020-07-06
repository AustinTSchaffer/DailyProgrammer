from typing import List

class Solution(object):
    def plusOne(self, digits):
        return plus_one(digits)

def plus_one(digits: List[int]) -> List[int]:
    current_digit = -1
    carry = True

    while carry:
        carry = False

        if abs(current_digit) > len(digits):
            # In the case of all-9s or empty list
            digits.insert(0, 1)

        elif digits[current_digit] == 9:
            # If the current digit is 9, add with carry
            digits[current_digit] = 0
            current_digit -= 1
            carry = True

        else:
            # increment current digit
            digits[current_digit] += 1

    return digits
