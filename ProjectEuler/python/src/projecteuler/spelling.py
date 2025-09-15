numbers = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
]

decade_prefixes = [
    None,
    None,
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety"
]

def spell(n: int) -> list[str]:
    if n > 9999:
        raise NotImplementedError()

    spelling = []

    if n >= 1000:
        left = n // 1000
        spelling.extend([numbers[left], "thousand"])
        
        n = n % 1000

    needs_and = False
    has_and = False
    if n >= 100:
        left = n // 100
        spelling.extend([numbers[left], "hundred"])
        needs_and = True
        n = n % 100

    if n >= 20:
        if needs_and and not has_and:
            spelling.append("and")
            has_and = True
        
        left = n // 10
        spelling.append(decade_prefixes[left])
        n = n % 10

    if n >= 1:
        if needs_and and not has_and:
            spelling.append("and")
            has_and = True

        spelling.append(numbers[n])

    return spelling
