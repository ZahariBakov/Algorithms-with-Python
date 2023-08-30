nums = [int(x) for x in input().split()]

is_sorted = False
interaction = len(nums)

while not is_sorted:
    is_sorted = True

    for idx in range(1, interaction):
        if nums[idx] < nums[idx - 1]:
            nums[idx], nums[idx - 1] = nums[idx - 1], nums[idx]
            is_sorted = False

    interaction -= 1

print(*nums, sep=' ')
