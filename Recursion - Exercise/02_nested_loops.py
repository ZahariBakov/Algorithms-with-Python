def nested_loops(idx, arr, result):
    if idx >= len(arr):
        result.append(' '.join(str(x) for x in arr))
        return

    for num in range(1, len(arr) + 1):
        arr[idx] = num
        nested_loops(idx + 1, arr, result)


def get_nested_loops(number):
    result = []
    nested_loops(0, [None] * number, result)
    return result


def main():
    number = int(input())

    for line in get_nested_loops(number):
        print(line)


if __name__ == '__main__':
    main()
