MAX_RESULT = OVERFLOW_RESULT = 2147483647 # pow(2, 31) - 1
MIN_RESULT = -2147483648 # -pow(2, 31)

class Solution:
    def divide(self, numerator: int, denominator: int) -> int:
        negative_output = (
            ((numerator < 0) and (denominator > 0)) or
            ((numerator > 0) and (denominator < 0))
        )

        numerator = abs(numerator)
        denominator = abs(denominator)

        if denominator > numerator:
            return 0

        quotient = 0
        remainder = 0

        numerator_bits = len(bin(numerator)) - 2

        for i in range(numerator_bits - 1, -1, -1):
            # Bit shift remainder left
            remainder = remainder << 1

            # Set the least-significant bit of R equal to bit i of the numerator
            remainder = set_bit(remainder, 0, get_bit(numerator, i))

            if remainder >= denominator:
                remainder -= denominator
                quotient = set_bit(quotient, i, True)

        result = (
            -quotient if negative_output else
            quotient
        )

        if result > MAX_RESULT or result < MIN_RESULT:
            return OVERFLOW_RESULT

        return result


def get_bit(number: int, position: int) -> bool:
    """
    Returns the nth bit of an integer as a boolean.

    0 refers to the LSB, aka 1s place.
    """
    return bool((number >> position) & 1)

def set_bit(number: int, position: int, value: bool) -> int:
    """
    Returns number if you were to set the nth bit to "value".

    0 refers to the LSB, aka 1s place.
    """
    return (
        (number | (1 << position)) if value else
        (number & ~(1 << position))
    )
