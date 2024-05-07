import functools

@functools.lru_cache()
def fib(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

def fib_iter(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1

    fib_n_m_2 = 0
    fib_n_m_1 = 1
    fib_n = 1
    for _ in range(n-2):
        fib_n_m_2 = fib_n_m_1
        fib_n_m_1 = fib_n
        fib_n = fib_n_m_1 + fib_n_m_2

    return fib_n

if __name__ == '__main__':
    print(fib_iter(0))
    print(fib_iter(1))
    print(fib_iter(2))
    print(fib_iter(3))
    print(fib_iter(4))
    print(fib_iter(5))
    print(fib_iter(6))
