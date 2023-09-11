from collections import deque

first_string = input()
second_string = input()

rows = len(first_string) + 1
cols = len(second_string) + 1

lcs = []
for _ in range(rows):
    lcs.append([0] * cols)

for row in range(1, rows):
    for col in range(1, cols):
        if first_string[row - 1] == second_string[col - 1]:
            lcs[row][col] = lcs[row - 1][col - 1] + 1
        else:
            lcs[row][col] = max(lcs[row -1][col], lcs[row][col - 1])

print(lcs[rows - 1][cols - 1])

# If we want to extract the elements.
row = rows - 1
col = cols - 1

result = deque()

while row > 0 and col > 0:
    if first_string[row - 1] == second_string[col - 1]:
        result.appendleft(first_string[row - 1]) # second[col - 1]
        row -= 1
        col -= 1
    elif lcs[row - 1][col] > lcs[row][col -1]:
        row -= 1
    else:
        col -= 1

print(result)