def calc_binom(n, k, memo):
    if k > n:
        return 0

    key = f"{n} {k}"

    if key in memo:
        return memo[key]

    if n == 0 or k == 0 or n == k:
        return 1

    result = calc_binom(n - 1, k - 1, memo) + calc_binom(n - 1, k, memo)
    memo[key] = result

    return result


def main():
    n = int(input())
    k = int(input())

    print(calc_binom(n, k, {}))


if __name__ == '__main__':
    main()
