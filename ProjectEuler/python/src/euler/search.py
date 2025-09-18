def binary_search(haystack: list, needle) -> bool:
    L = 0
    R = len(haystack) - 1

    while L <= R:
        M = ((R - L) // 2) + L
        current = haystack[M]
        if current == needle:
            return True
        if needle < current:
            R = M - 1
        if needle > current:
            L = M + 1

    return False
