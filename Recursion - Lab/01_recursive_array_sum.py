def array_sum(nums, idx):
    if idx == len(nums) - 1:
        return nums[idx]

    return nums[idx] + array_sum(nums, idx + 1)


def main():
    nums = [int(x) for x in input().split()]

    print(array_sum(nums, 0))


if __name__ == '__main__':
    main()
