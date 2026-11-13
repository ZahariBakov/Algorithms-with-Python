def insertion_sort(nums):
    for i in range(1, len(nums)):
        for j in range(i, 0, -1):
            if nums[j] < nums[j - 1]:
                nums[j], nums[j - 1] = nums[j - 1], nums[j]
            else:
                break

    return nums


def main():
    nums = [int(x) for x in input().split()]

    print(*insertion_sort(nums), sep=" ")


if __name__ == '__main__':
    main()
