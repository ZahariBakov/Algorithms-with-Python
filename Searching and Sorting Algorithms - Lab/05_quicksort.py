def quick_sort(start, end, array):
    if start >= end:
        return

    pivot = start
    left = start + 1
    right = end

    while left <= right:
        if array[left] > array[pivot] > array[right]:
            array[left], array[right] = array[right], array[left]

        if array[left] <= array[pivot]:
            left += 1

        if array[right] >= array[pivot]:
            right -= 1

    array[pivot], array[right] = array[right], array[pivot]
    quick_sort(start, right - 1, array)
    quick_sort(left, end, array)

nums = [int(x) for x in input().split()]

quick_sort(0, len(nums) - 1, nums)

print(*nums, sep=" ")
