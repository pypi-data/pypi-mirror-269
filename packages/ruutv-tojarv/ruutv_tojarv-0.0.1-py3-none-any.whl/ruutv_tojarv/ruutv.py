import math


def solve(a, b, c):
    if a == 0:
        print("Incorrect")
        return 0

    d = b * b - 4 * a * c
    sqrt_value = math.sqrt(abs(d))

    if d > 0:
        answ1 = (-b + sqrt_value) / (2 * a)
        answ2 = (-b - sqrt_value) / (2 * a)
        return answ1, answ2

    elif d == 0:
        answ = -b / (2 * a)
        return answ

    else:
        return 0




