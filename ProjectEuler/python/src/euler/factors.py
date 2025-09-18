import math
from euler import sequences


def distinct_prime_factors(n):
    factors_ = []
    half_n = n / 2
    for prime in sequences.primes():
        if prime > half_n:
            break
        if n % prime == 0:
            factors_.append(prime)
    return factors_


_is_prime_cache = set()
_is_prime_max_prime: int = 0
_is_prime_prime_generator = sequences.primes()


def is_prime(n: int) -> bool:
    global _is_prime_max_prime

    n = abs(n)

    while n > _is_prime_max_prime:
        _is_prime_max_prime = next(_is_prime_prime_generator)
        _is_prime_cache.add(_is_prime_max_prime)

    return n in _is_prime_cache


def factors(n, proper=False):
    factors_ = [1]
    sqrt_n = math.sqrt(n)
    for i in range(2, n):
        if i > sqrt_n:
            break
        if n % i == 0:
            factors_.append(i)

    if factors_[-1] * factors_[-1] == n:
        for f in reversed(factors_[:-1]):
            if f == 1 and proper:
                continue
            factors_.append(n // f)
    else:
        for f in reversed(factors_):
            if f == 1 and proper:
                continue
            factors_.append(n // f)

    return factors_


def num_factors(n, proper=False):
    if n == 1:
        return 1

    last_factor = 0
    n_factors = 1
    sqrt_n = int(math.sqrt(n))
    for i in range(2, n):
        if i > sqrt_n:
            break
        if n % i == 0:
            n_factors += 1
            last_factor = i

    if last_factor * last_factor == n:
        n_factors += n_factors - 1
    else:
        n_factors += n_factors

    if proper:
        n_factors -= 1

    return n_factors


def long_division(numerator: int, denominator: int, precision: int) -> list[int]:
    """
    Performs long division to the specified precision. The first index of
    the output will be the whole-number part of the result. The remaining
    indices will be the decimal notation of the fractional component.
    """

    fraction = []
    fractional_digits = 0

    while fractional_digits <= precision:
        if numerator == 0:
            break

        while numerator < denominator:
            numerator *= 10
            fraction.append(0)
            fractional_digits += 1

        fraction.append(numerator // denominator)
        fractional_digits += 1
        numerator = (numerator % denominator) * 10

    return fraction
