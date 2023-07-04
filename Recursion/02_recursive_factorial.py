def calc_fact(n):
    if n == 1:
        return 1

    return n * calc_fact(n - 1)


def iterative_fact(n):
    result = 1

    for num in range(1, n + 1):
        result *= num

    return result


num = int(input())

print(calc_fact(num))
print(iterative_fact(num))

