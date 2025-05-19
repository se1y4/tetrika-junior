from solution import strict

@strict
def sum_two(a: int, b: int) -> int:
    return a + b

print(sum_two(1, 2))
print(sum_two(1, 1.5))
print(sum_two(1, '1'))