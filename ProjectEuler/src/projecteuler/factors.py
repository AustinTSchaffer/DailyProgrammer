import math
from projecteuler import sequences

def prime_factors(n):
    factors_ = []
    sqrt_n = math.sqrt(n)
    for prime in sequences.primes():
        if prime > sqrt_n:
            break
        if n % prime == 0:
            factors_.append(prime)
    return factors_

def factors(n):
    factors_ = [1]
    sqrt_n = math.sqrt(n)
    for i in range(2, n):
        if i > sqrt_n:
            break
        if n % i == 0:
            factors_.append(i)

    if factors_[-1] * factors_[-1] == n:
        for f in reversed(factors_[:-1]):
            factors_.append(n // f)
    else:
        for f in reversed(factors_):
            factors_.append(n // f)

    return factors_

def num_factors(n):
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
        n_factors += (n_factors - 1)
    else:
        n_factors += n_factors

    return n_factors
