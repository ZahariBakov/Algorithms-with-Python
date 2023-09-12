replace_cost = int(input())
insert_cost = int(input())
delete_cost = int(input())
first_string = input()
second_string = input()

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

print(f"Minimum edit distance: {dp[rows - 1][cols - 1]}")

for row in dp:
    print(row)
