import math


def fibonacci():
    yield 1
    yield 1

    n_1 = 1
    n_2 = 1
    while True:
        n = n_1 + n_2
        n_2 = n_1
        n_1 = n
        yield n


def primes():
    """
    Generate an infinite sequence of prime numbers using the
    Sieve of Eratosthenes method. (Stolen from Stack Overflow).
    """

    # Maps composites to primes witnessing their compositeness.
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1


def triangle_numbers():
    n = 1
    v = 1

    while True:
        yield v
        n += 1
        v += n


def next_collatz(n):
    if n % 2 == 0:
        n = n // 2
    else:
        n = (3 * n) + 1
    return n


def collatz(n):
    while True:
        yield n
        if n == 1:
            break
        n = next_collatz(n)


def seq_less_than(seq, n: int | float, or_equal=False):
    if callable(seq):
        seq = seq()
    for v in seq:
        if or_equal:
            if v > n:
                break
        elif v >= n:
            break
        yield v


def seq_first_n(seq, n: int):
    if callable(seq):
        seq = seq()

    for _ in range(n):
        yield next(seq)
