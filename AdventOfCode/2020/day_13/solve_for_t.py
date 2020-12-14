# Modulus operations to check values of t
def check_t(t):
    return (
        ((t + 19) % 787 == 0) and
        ((t + 50) % 571 == 0) and
        ((t + 9) % 41 == 0) and
        ((t + 13) % 37 == 0) and
        ((t + 48) % 29 == 0) and
        ((t + 42) % 23 == 0) and
        ((t + 0) % 19 == 0) and
        ((t + 67) % 17 == 0) and
        ((t + 32) % 13 == 0)
    )

D = 0
t = -1

while not check_t(t):
    # Equation for t in terms of d, incrementing d by 164749 each time.
    D = D + 164749
    t = (D * 787) - 19

print("t =", t)
