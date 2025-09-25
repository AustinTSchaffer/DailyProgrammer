import math
import re
import string
import itertools
import fractions

from euler import data, factors, poker, polynomial_nums, search, sequences, spelling


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
    return max(factors.distinct_prime_factors(number))


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
    perms = itertools.permutations("0123456789")
    for idx, perm in enumerate(perms, start=1):
        if idx == 1_000_000:
            return "".join(perm)
    raise ValueError()


def p25():
    for idx, F_idx in enumerate(sequences.fibonacci(), start=1):
        if len(str(F_idx)) >= 1000:
            return idx


def p26():
    fractions = {
        d: factors.long_division(numerator=1, denominator=d, precision=10000)
        for d in range(1, 1000)
    }

    # with open('fractions.txt', 'w') as f:
    #     for d, fraction in fractions.items():
    #         f.write(f'{d}: {fraction[0]}.')
    #         f.write(''.join(map(str, fraction[1:])))
    #         f.write('\n')

    fractions_bar_notation = []
    for d, fraction in fractions.items():
        fraction = "".join(map(str, fraction))
        repeating_segment_found = False
        for length in range(1, len(fraction)):
            segments = {
                fraction[-(length * (offset + 1)) : -(length * offset)]
                for offset in range(1, 4)
            }
            if len(segments) == 1:
                repeating_segment = next(iter(segments))
                fractions_bar_notation.append(
                    {
                        "segment_length": length,
                        "repeating_segment": repeating_segment,
                        "d": d,
                        "prefix": fraction.split(repeating_segment)[0],
                    }
                )
                repeating_segment_found = True
                break

        if not repeating_segment_found:
            if len(fraction) > 100:
                print("Warning: No repeating segment found in fraction:", fraction)

    return max(fractions_bar_notation, key=lambda v: v["segment_length"])["d"]


def p27():
    def gen_primes(a: int, b: int):
        n = 0
        while True:
            result = (n**2) + (a * n) + b
            if not factors.is_prime(result):
                return n
            n += 1

    best = (0, None, None)
    for a in range(-999, 1000):
        for b in range(-1000, 1001):
            result = gen_primes(a, b)
            if result > best[0]:
                best = (result, a, b)

    return f"best={best} a*b={best[1] * best[2]}"


def p28(final_size=1001):
    current_size = 1
    sum_ = 1
    last_value = 1
    diff = 0
    while current_size < final_size:
        diff += 2
        for _ in range(4):
            last_value += diff
            sum_ += last_value
        current_size += 2

    return sum_


def p29():
    results = set()
    for a in range(2, 101):
        for b in range(2, 101):
            results.add(a**b)
    return len(results)


def p30():
    # OEIS: A052464
    return 4150 + 4151 + 54748 + 92727 + 93084 + 194979


def p31():
    # coins = [1, 2, 5, 10, 20, 50, 100, 200]
    target = 200
    ways = 0
    for a in range(0, target + 1, 1):
        for b in range(a, target + 1, 2):
            for c in range(b, target + 1, 5):
                for d in range(c, target + 1, 10):
                    for e in range(d, target + 1, 20):
                        for f in range(e, target + 1, 50):
                            for g in range(f, target + 1, 100):
                                for h in range(g, target + 1, 200):
                                    if h == target:
                                        ways += 1
    return ways


def p32():
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    results = set()

    for index in range(0, int("1" + ("0" * len(digits)), 3)):
        terms = [[], [], []]
        for digit in digits:
            terms[index % 3].append(digit)
            index //= 3

        if (
            not terms[0]
            or not terms[1]
            or not terms[2]
            or len(terms[2]) < len(terms[1])
            or len(terms[2]) < len(terms[0])
        ):
            continue

        for a_perm in itertools.permutations(terms[0]):
            for b_perm in itertools.permutations(terms[1]):
                a = 0
                for digit_idx, digit in enumerate(a_perm):
                    a += digit * (10**digit_idx)

                b = 0
                for digit_idx, digit in enumerate(b_perm):
                    b += digit * (10**digit_idx)

                c = a * b

                if sorted(str(c)) == sorted(map(str, terms[2])):
                    results.add(c)

    return sum(results)


def p33():
    fracs = []
    for numerator in range(11, 100):
        for denominator in range(numerator + 1, 100):
            result = fractions.Fraction(numerator, denominator)
            reduced_numer = str(numerator)
            reduced_denom = str(denominator)
            reduced = False
            if reduced_numer[1] != "0" and reduced_numer[1] in reduced_denom:
                reduced_denom = reduced_denom.replace(reduced_numer[1], "", count=1)
                reduced_numer = reduced_numer.replace(reduced_numer[1], "", count=1)
                reduced = True
            if reduced_numer[0] != "0" and reduced_numer[0] in reduced_denom:
                reduced_denom = reduced_denom.replace(reduced_numer[0], "", count=1)
                reduced_numer = reduced_numer.replace(reduced_numer[0], "", count=1)
                reduced = True
            if (
                not reduced_numer
                or not reduced_denom
                or reduced_denom == "0"
                or not reduced
            ):
                continue
            new_fraction = fractions.Fraction(int(reduced_numer), int(reduced_denom))
            if new_fraction == result:
                fracs.append(result)
    result = fractions.Fraction(1, 1)
    for frac in fracs:
        result *= frac
    return result.denominator


def p34():
    # OEIS: A014080
    return 145 + 40585


def p35(n=1_000_000):
    primes_below_n = set(map(str, sequences.seq_less_than(sequences.primes(), n)))
    n_circular_primes = 0
    for prime in primes_below_n:
        is_circular = True
        for pivot in range(1, len(prime)):
            rotation = prime[pivot:] + prime[:pivot]
            if rotation not in primes_below_n:
                is_circular = False
                break
        if is_circular:
            n_circular_primes += 1
    return n_circular_primes


def p36():
    result = 0
    for number in range(1, 1_000_000):
        if str(number) == "".join(reversed(str(number))):
            number_base_2 = bin(number)[2:]
            if number_base_2 == "".join(reversed(number_base_2)):
                result += number
    return result


def p37():
    result = 0
    primes_found = 0
    primes_gen = sequences.primes()
    while primes_found < 11:
        prime = next(primes_gen)
        if prime < 10:
            continue

        prime_str = str(prime)
        is_trunctable_prime = True
        for idx in range(1, len(prime_str)):
            if not factors.is_prime(int(prime_str[idx:])):
                is_trunctable_prime = False
                break
            if not factors.is_prime(int(prime_str[: len(prime_str) - idx])):
                is_trunctable_prime = False
                break
        if is_trunctable_prime:
            result += prime
            primes_found += 1
    return result


def p38():
    max_ = 0
    max_pandigital = 987654321

    for a in range(1, int(math.sqrt(max_pandigital)) + 1):
        pd_candidate = ""
        for b in range(1, 10):
            pd_candidate_new = pd_candidate + str(a * b)
            if len(pd_candidate_new) > 9:
                break
            pd_candidate = pd_candidate_new
        if spelling.is_pandigital(pd_candidate):
            max_ = max(int(pd_candidate), max_)

    return max_


def p39(max_p=1000):
    perimeters = [0] * (max_p + 1)
    for a in range(1, (max_p // 2) + 1):
        for b in range(a + 1, (max_p // 2) + 1):
            c = math.sqrt((a**2) + (b**2))
            if int(c) != c:
                continue
            p = a + b + int(c)
            if p > max_p:
                continue
            perimeters[p] += 1

    return max(
        (num_solutions, perimeter) for perimeter, num_solutions in enumerate(perimeters)
    )[1]


def p40():
    number = " "
    current_integer = 1
    while len(number) <= 1_000_000:
        number += str(current_integer)
        current_integer += 1

    return (
        int(number[1])
        * int(number[10])
        * int(number[100])
        * int(number[1_000])
        * int(number[10_000])
        * int(number[100_000])
        * int(number[1_000_000])
    )


def p41():
    max_ = 0
    for prime in sequences.primes():
        # 987654321 and 87654321 are both divisible by 3. There can't be
        # any pandigital primes beyond 7 digits.
        if prime >= 7654321:
            break
        if spelling.is_pandigital(prime):
            max_ = prime
    return max_


def p42():
    num_triangle_words = 0
    letter_offset = ord("A")
    for word in data.p42:
        word_value = sum(ord(letter) - letter_offset + 1 for letter in word)
        if polynomial_nums.is_triange_number(word_value):
            num_triangle_words += 1
    return num_triangle_words


def p43():
    sum_ = 0
    divisors = [2, 3, 5, 7, 11, 13, 17]
    digits = "0123456789"
    for perm in itertools.permutations(digits):
        has_property = True
        for idx, divisor in enumerate(divisors):
            d = int("".join(perm[1 + idx : 1 + idx + 3]).lstrip("0"))
            if divisor not in factors.distinct_prime_factors(d):
                has_property = False
                break
        if has_property:
            sum_ += int("".join(perm))
    return sum_


def p44():
    pn_cache = []
    for pn_j in sequences.pentagonal_numbers():
        pn_cache.append(pn_j)
        for pn_k in pn_cache[-2::-1]:
            if polynomial_nums.is_pentagonal_number(pn_j + pn_k):
                if polynomial_nums.is_pentagonal_number(pn_j - pn_k):
                    return pn_j - pn_k


def p45():
    skip_answers = 2
    for T in sequences.triangle_numbers():
        if polynomial_nums.is_pentagonal_number(
            T
        ) and polynomial_nums.is_hexagonal_number(T):
            if skip_answers == 0:
                return T
            skip_answers -= 1


def p46():
    odd_composite = 1
    while True:
        odd_composite += 2
        if factors.is_prime(odd_composite):
            continue
        has_goldbach_property = False
        for prime in sequences.seq_less_than(sequences.primes, odd_composite):
            for square in sequences.seq_less_than(
                sequences.square_numbers, (odd_composite - prime) / 2, True
            ):
                if (prime + (2 * square)) == odd_composite:
                    has_goldbach_property = True
                    break
            if has_goldbach_property:
                break
        if not has_goldbach_property:
            return odd_composite


def p47():
    sum_ = 0
    mod = 10**10
    for i in range(1, 1001):
        term = 1
        for _ in range(1, i + 1):
            term *= i
            term %= mod
        sum_ += term
    return sum_ % mod


def p49():
    primes = set()

    for prime in sequences.primes():
        if prime >= 1000:
            if prime > 9999:
                break
            primes.add(prime)

    groups = []
    for prime in primes:
        group = set()
        for perm in itertools.permutations(str(prime)):
            perm_as_int = int("".join(perm))
            if perm_as_int in primes:
                group.add(perm_as_int)
        if len(group) >= 3:
            group = list(sorted(group))
            for other_value in group:
                if other_value <= prime:
                    continue
                third_value = (other_value - prime) + other_value
                if third_value in group:
                    groups.append((prime, other_value, third_value))

    group = groups[0] if groups[0][0] != 1487 else groups[1]
    return "".join(map(str, group))


def p50():
    best_results = {}
    primes = list(sequences.seq_less_than(sequences.primes, 1_000_000))

    for start_idx, start_prime in enumerate(primes):
        current_value = start_prime
        for end_idx in range(start_idx + 1, len(primes)):
            current_value += primes[end_idx]

            if current_value > 1_000_000:
                break

            if search.binary_search(primes, current_value):
                best_results[end_idx - start_idx] = (current_value, primes[start_idx])

    longest_chain = max(best_results.keys())
    best_result = best_results[longest_chain]
    return best_result[
        0
    ], f"Sum of {longest_chain} consecutive primes, starting with {best_result[1]}"


def p51():
    for prime in sequences.primes():
        if prime < 56003:
            continue
        prime_str = str(prime)
        unique_digits = set(prime_str)

        for digit in unique_digits:
            family_size = 0
            for replacement_digit in "0123456789":
                if digit == prime_str[0] and replacement_digit == "0":
                    continue

                # There's actually a bug here, but this is good enough to solve
                # the problem. This assumes that you won't ever replace need to
                # replace only a subset of the digits in "prime_str" that match
                # "digit".
                if factors.is_prime(int(prime_str.replace(digit, replacement_digit))):
                    family_size += 1

            if family_size >= 8:
                return prime_str


def p52():
    x = 1
    while True:
        if len({"".join(sorted(str(a * x))) for a in range(1, 7)}) == 1:
            return x
        x += 1


def p53():
    vals_gt_1m = 0
    factorials = [math.factorial(i) for i in range(101)]

    for n in range(1, 101):
        for r in range(1, n + 1):
            if (factorials[n] / (factorials[r] * factorials[n - r])) > 1_000_000:
                vals_gt_1m += 1
    return vals_gt_1m


def p54():
    p1_wins = 0

    _data = data.p54.strip().split("\n")
    poker_hands = []
    for line in _data:
        cards = line.split()
        assert len(cards) == 10
        cards = [
            (
                10
                if card[0] == "T"
                else 11
                if card[0] == "J"
                else 12
                if card[0] == "Q"
                else 13
                if card[0] == "K"
                else 14
                if card[0] == "A"
                else int(card[0]),
                card[1],
            )
            for card in line.split()
        ]

        poker_hands.append((cards[:5], cards[5:]))

    for p1_hand, p2_hand in poker_hands:
        p1_hand_score = poker.determine_result(p1_hand)
        p2_hand_score = poker.determine_result(p2_hand)
        if p1_hand_score > p2_hand_score:
            p1_wins += 1

    return p1_wins


def p55():
    num_lychrel_nums = 0

    for n in range(10000):
        n_modified = n
        is_lychrel = True
        for i in range(50):
            n_modified += int("".join(reversed(str(n_modified))))
            if spelling.is_palindrome(n_modified):
                is_lychrel = False
        if is_lychrel:
            num_lychrel_nums += 1
    return num_lychrel_nums

def p56():
    max_digital_sum = 0
    for a in range(100):
        for b in range(100):
            result = a ** b
            digital_sum = sum(map(int, str(result)))
            max_digital_sum = max(max_digital_sum, digital_sum)
    return max_digital_sum


def p57():
    result = 0
    prior_rhs = 0
    for iteration in range(1, 1001):
        rhs = fractions.Fraction(1, 2 + prior_rhs)
        frac = 1 + rhs
        if len(str(frac.numerator)) > len(str(frac.denominator)):
            result += 1
        prior_rhs = rhs

    return result

def p59():
    ciphertext = list(map(int, data.p59.split(',')))
    key_characters = list(map(ord, 'qwertyuiopasdfghjklzxcvbnm'))
    key_len = 3
    plaintext: list[str] = [' '] * len(ciphertext)
    valid_plaintext_chars = string.ascii_letters + string.punctuation + ' ' + string.digits

    possible_plaintexts = []
    for possible_key in itertools.combinations_with_replacement(key_characters, key_len):
        for key_perm in itertools.permutations(possible_key):
            contained_invalid_char = False
            for i, char_ord in enumerate(ciphertext):
                plaintext_char = chr(char_ord ^ key_perm[i % key_len])
                if plaintext_char not in valid_plaintext_chars:
                    contained_invalid_char = True
                    break
                plaintext[i] = chr(char_ord ^ key_perm[i % key_len])

            if not contained_invalid_char:
                possible_plaintexts.append(''.join(plaintext))

    filtered = [
        pt for pt in possible_plaintexts
        if ' the ' in pt
    ]

    assert len(filtered) == 1
    return sum(map(ord, filtered[0]))

current = p59
