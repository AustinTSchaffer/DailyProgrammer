import math

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
