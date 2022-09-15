from math import factorial


def count_elements_in_sequence(n: int, k: int) -> int:
    if k <= 0 or n < 0:
        return 0
    count_permutations = int(factorial(k) / factorial(k - 2)) if k > 1 else 0
    return n * k * 2 + count_permutations + 1
