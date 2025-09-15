from projecteuler import factors, sequences, data, spelling
import re
import math
import multiprocessing


def p2():
    sum_ = 0
    for n in sequences.fibonacci():
        if n > 4_000_000:
            break
        if n % 2 == 0:
            sum_ += n
    return sum_


def p3():
    number = 600_851_475_143
    return max(factors.prime_factors(number))


def p4():
    max_p = 0
    for a in range(999, 100, -1):
        for b in range(a, 100, -1):
            n = a * b
            if n <= max_p:
                continue
            n_str = str(n)
            n_str_rev = "".join(reversed(n_str))
            if n_str == n_str_rev:
                max_p = n
    return max_p


def p5():
    factors = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    n = 2520
    while True:
        is_answer = True
        for factor in factors:
            if n % factor != 0:
                is_answer = False
                break
        if is_answer:
            return n
        n += 20


def p6():
    sum_of_the_squares = 0
    sum_of_the_numbers = 0
    for i in range(1, 101):
        sum_of_the_numbers += i
        sum_of_the_squares += i**2

    square_of_the_sum = sum_of_the_numbers**2
    return square_of_the_sum - sum_of_the_squares


def p7():
    first_10k_primes = list(zip(range(1, 10002), sequences.primes()))
    print("6th: ", first_10k_primes[5])
    return first_10k_primes[10_000]


def p8():
    data_ = data.p8

    def consecutive_digits(n):
        i = 0
        while (i + n) <= len(data_):
            yield list(map(int, data_[i : i + n]))
            i += 1

    return max((math.prod(seq), seq) for seq in consecutive_digits(13) if 0 not in seq)


def p9():
    for a in range(1, 998):
        for b in range(a + 1, 999):
            c = (1000 - a) - b
            if c == a or c == b:
                continue
            if ((a**2) + (b**2)) != (c**2):
                continue
            return a * b * c


def p10():
    return sum(sequences.seq_less_than(sequences.primes, 2_000_000))


def p11():
    grid: list[list[int]] = []

    for line in data.p11.splitlines():
        if not line.strip():
            continue
        grid.append(list(map(int, re.findall(r"\d{2}", line))))

    def horiz(n=4):
        for row in range(0, len(grid)):
            for col in range(0, len(grid[row]) - n + 1):
                yield grid[row][col : col + 4]

    def vert(n=4):
        for row in range(0, len(grid) - n + 1):
            for col in range(0, len(grid[row])):
                yield [grid[row + i][col] for i in range(n)]

    def diag(n=4):
        for row in range(0, len(grid) - n + 1):
            for col in range(0, len(grid[row]) - n + 1):
                yield [grid[row + i][col + i] for i in range(n)]

    def rev_diag(n=4):
        for row in range(n - 1, len(grid)):
            for col in range(0, len(grid[row]) - n + 1):
                yield [grid[row - i][col + i] for i in range(n)]

    return max(
        (math.prod(adj_nums), adj_nums)
        for iterator in [horiz(), vert(), diag(), rev_diag()]
        for adj_nums in iterator
    )


def p12():
    for tn in sequences.triangle_numbers():
        divisors = factors.num_factors(tn)
        if divisors > 500:
            return tn


def p13():
    return str(sum(map(int, filter(bool, data.p13.splitlines()))))[:10]


def p14():
    _collatz_seq_lens: dict[int, int] = {}

    def collatz_seq_len(n):
        current_n = n
        iters = 0
        while current_n != 1:
            current_n = sequences.next_collatz(current_n)
            iters += 1
            if current_n in _collatz_seq_lens:
                print(iters)
                _collatz_seq_lens[n] = iters + _collatz_seq_lens[current_n]
                return _collatz_seq_lens[n]
        _collatz_seq_lens[n] = iters
        return iters

    max_ = (0, 1)
    for i in range(1, 1_000_000):
        length = collatz_seq_len(i)
        if length > max_[0]:
            max_ = (length, i)

    return max_


def p15(n=20):
    # Fencepost problem
    n += 1

    grid = []
    for _ in range(n):
        grid.append([None] * n)
    for i in range(n):
        grid[0][i] = 1
        grid[i][0] = 1
    for i in range(1, n):
        for j in range(1, n):
            grid[i][j] = grid[i - 1][j] + grid[i][j - 1]
    return grid[-1][-1]


def p16(power=1000):
    value = 1
    for _ in range(power):
        value *= 2
    return sum(map(int, str(value)))


def p17(max=1000):
    letter_count = 0
    for i in range(max, 0, -1):
        number_name = spelling.spell(i)
        for word in number_name:
            letter_count += len(word)
    return letter_count


def p18():
    triangle = []
    for row in data.p18.splitlines():
        if not row:
            continue
        triangle.append(list(map(int, row.split())))

    for row_idx in range(len(triangle) - 2, -1, -1):
        for idx in range(len(triangle[row_idx])):
            triangle[row_idx][idx] += max(
                triangle[row_idx + 1][idx],
                triangle[row_idx + 1][idx + 1],
            )

    return triangle[0][0]


def p19():
    import datetime

    count = 0
    for year in range(1901, 2001):
        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            if date.isoweekday() == 7:
                count += 1
    return count


def p20(n=100):
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i
        while fact % 10 == 0:
            fact //= 10
    return sum(map(int, str(fact)))


def p21():
    a_n_cache = {}

    def amicable_number(n):
        if n in a_n_cache:
            return a_n_cache[n]
        a_n_cache[n] = sum(factors.factors(n, proper=True))
        return a_n_cache[n]

    sum_ = 0
    for a in range(2, 10_001):
        b = amicable_number(a)
        if a != b and b <= 10_000 and amicable_number(b) == a:
            # print('Amicable Pair:', a, b)
            sum_ += a
            sum_ += b

    # Overcounted
    return sum_ // 2


def p22():
    names = sorted(data.p22)
    offset = ord("A") - 1
    total = 0
    for idx, name in enumerate(names, start=1):
        total += sum(ord(letter) - offset for letter in name) * idx

    return total


def p23():
    abundant_numbers_set = [False]
    abundant_numbers_list = []
    for n in range(1, 28124):
        is_abundant = sum(factors.factors(n, proper=True)) > n
        abundant_numbers_set.append(is_abundant)
        if is_abundant:
            abundant_numbers_list.append(n)

    total = 0
    for n in range(1, 28124):
        print(n)
        is_sum_of_2_abundant_nums = False
        for an in abundant_numbers_list:
            if an > n:
                break
            if abundant_numbers_set[n - an]:
                is_sum_of_2_abundant_nums = True
                break
        if not is_sum_of_2_abundant_nums:
            total += n

    return total


def p24():
    import itertools

    perms = itertools.permutations("0123456789")
    for idx, perm in enumerate(perms, start=1):
        if idx == 1_000_000:
            return ''.join(perm)
    raise ValueError()


def p25():
    for idx, F_idx in enumerate(sequences.fibonacci(), start=1):
        if len(str(F_idx)) >= 1000:
            return idx

def p26():
    ...

current = p25
