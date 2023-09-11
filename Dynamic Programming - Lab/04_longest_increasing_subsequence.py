from collections import deque

nums = [int(x) for x in input().split()]

length = len(nums)

size = [0] * length
size[0] = 1

parent = [None] * length

best_idx = 0
best_size = 1

for cur_idx in range(1, length):
    cur_num = nums[cur_idx]
    current_best_size = 1
    current_parent = None

    for prev_idx in range(cur_idx -1, -1, -1):
        prev_num = nums[prev_idx]

        if prev_num >= cur_num:
            continue

        if size[prev_idx] + 1 >= current_best_size:
            current_best_size = size[prev_idx] + 1
            current_parent = prev_idx

    size[cur_idx] = current_best_size
    parent[cur_idx] = current_parent

    if current_best_size > best_size:
        best_size = current_best_size
        best_idx = cur_idx

print(best_size)

result = deque()

while best_idx is not None:
    result.appendleft(nums[best_idx])
    best_idx = parent[best_idx]

print(*result, sep=" ")
