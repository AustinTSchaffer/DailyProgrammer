def fibonacci():
    yield 1
    yield 1

    n_1 = 1
    n_2 = 1
    while True:
        n = n_1 + n_2
        n_2 = n
        n_1 = n_2
        yield n_2
