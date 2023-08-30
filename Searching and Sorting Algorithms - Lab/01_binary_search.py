# Iterative decision:

# def binary_search(nums, target):
#     left = 0
#     right = len(nums) - 1
#
#     while left <= right:
#         mid_idx = (left + right) // 2
#         mid_el = nums[mid_idx]
#
#         if mid_el == target:
#             return mid_idx
#
#         if target > mid_el:
#             left = mid_idx + 1
#         else:
#             right = mid_idx - 1
#
#     return -1
#
#
# nums = [int(x) for x in input().split()]
# target = int(input())
#
# print(binary_search(nums, target))

# --------------------------------------------------------------------
# Recursive decision:

def binary_search(left, right, nums, target):
    if left <= right:
        mid_idx = (left + right) // 2
        mid_el = nums[mid_idx]
        if mid_el == target:
            return mid_idx

        if target > mid_el:
            return binary_search(mid_idx + 1, right, nums, target)
        else:
            return binary_search(left, mid_idx - 1, nums, target)
    else:
        return -1

nums = [int(x) for x in input().split()]
target = int(input())


print(binary_search(0, len(nums) -1, nums, target))
