def max_connected_pairs(cables):
    size = len(cables) + 1
    positions = [pos for pos in range(1, size)]

    lcs = []
    [lcs.append([0] * size) for _ in range(size)]

    for row in range(1, size):
        for col in range(1, size):
            if cables[row - 1] == positions[col - 1]:
                lcs[row][col] = lcs[row - 1][col - 1] + 1
            else:
                lcs[row][col] = max(lcs[row - 1][col], lcs[row][col -1])

    return lcs[size - 1][size - 1]


def main():
    cables = [int(x) for x in input().split()]

    print(f"Maximum pairs connected: {max_connected_pairs(cables)}")


if __name__ == '__main__':
    main()
