def word_differences(first, second):
    dp = []
    rows = len(first) + 1
    cols = len(second) + 1

    for _ in range(rows):
        dp.append([0] * cols)

    for col in range(1, cols):
        dp[0][col] = col

    for row in range(1, rows):
        dp[row][0] = row

    for row in range(1, rows):
        for col in range(1, cols):
            if first[row - 1] == second[col - 1]:
                dp[row][col] = dp[row - 1][col - 1]
            else:
                dp[row][col] = min(dp[row][col - 1], dp[row - 1][col]) + 1

    return dp[rows -1][cols - 1]


def main():
    first = input()
    second = input()

    print(f"Deletions and Insertions: {word_differences(first, second)}")


if __name__ == '__main__':
    main()
