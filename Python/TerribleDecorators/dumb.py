import functools

def add(n):
    def _(f):
        @functools.wraps(f)
        def __(*a, **b):
            return f(*a, **b) + n
        return __
    return _

def multiply(n):
    def _(f):
        @functools.wraps(f)
        def __(*a, **b):
            return f(*a, **b) * n
        return __
    return _

def subtract(n):
    def _(f):
        @functools.wraps(f)
        def __(*a, **b):
            return f(*a, **b) - n
        return __
    return _

def divide(n):
    def _(f):
        @functools.wraps(f)
        def __(*a, **b):
            return f(*a, **b) / n
        return __
    return _

def square():
    def _(f):
        @functools.wraps(f)
        def __(*a, **b):
            return f(*a, **b) ** 2
        return __
    return _

def pow(n):
    def _(f):
        @functools.wraps(f)
        def __(*a, **b):
            return f(*a, **b) ** n
        return __
    return _

def quadratic(a, b, c):
    @multiply(-1)
    @add(b)
    def negative_b():
        return 0

    @multiply(b)
    @multiply(a)
    @multiply(4)
    @add(1)
    def four_a_c():
        return 0

    @pow(0.5)
    @subtract(four_a_c())
    @pow(2)
    @add(b)
    def sqrt_of_b_squared_minus_four_a_c():
        return 0

    @add(sqrt_of_b_squared_minus_four_a_c())
    @add(negative_b())
    def negative_b_plus_the_sqrt_of_b_squared_minus_four_a_c():
        return 0

    @subtract(sqrt_of_b_squared_minus_four_a_c())
    @add(negative_b())
    def negative_b_minus_the_sqrt_of_b_squared_minus_four_a_c():
        return 0

    @multiply(2)
    @add(a)
    def two_a():
        return 0

    @divide(two_a())
    @add(negative_b_minus_the_sqrt_of_b_squared_minus_four_a_c())
    def negative_b_minus_the_sqrt_of_b_squared_minus_four_a_c_over_two_a():
        return 0

    @divide(two_a())
    @add(negative_b_plus_the_sqrt_of_b_squared_minus_four_a_c())
    def negative_b_plus_the_sqrt_of_b_squared_minus_four_a_c_over_two_a():
        return 0

    x = (
        negative_b_plus_the_sqrt_of_b_squared_minus_four_a_c_over_two_a(),
        negative_b_minus_the_sqrt_of_b_squared_minus_four_a_c_over_two_a(),
    )

    return x
