def min_edit_distance(replace_cost, insert_cost, delete_cost, first_string, second_string):
    rows = len(first_string) + 1
    cols = len(second_string) + 1

    dp = []

    for _ in range(rows):
        dp.append([0] * cols)

    for col in range(1, cols):
        dp[0][col] = dp[0][col - 1] + insert_cost

    for row in range(1, rows):
        dp[row][0] = dp[row - 1][0] + delete_cost

    for row in range(1, rows):
        for col in range(1, cols):
            if first_string[row - 1] == second_string[col - 1]:
                dp[row][col] = dp[row - 1][col - 1]
            else:
                dp[row][col] = min(dp[row][col - 1] + insert_cost, dp[row - 1][col] + delete_cost,
                                   dp[row - 1][col - 1] + replace_cost)

    return dp[rows - 1][cols - 1]


def main():
    replace_cost = int(input())
    insert_cost = int(input())
    delete_cost = int(input())
    first_string = input()
    second_string = input()

    result = min_edit_distance(replace_cost, insert_cost, delete_cost, first_string, second_string)

    print(f"Minimum edit distance: {result}")


if __name__ == '__main__':
    main()
