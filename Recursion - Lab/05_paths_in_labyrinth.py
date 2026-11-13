def find_all_paths(row, col, lab, direction, path, result):
    # Check if current position is outside
    if row < 0 or col < 0 or row >= len(lab) or col >= len(lab[0]):
        return

    # Check if current position is 'WALL'
    if lab[row][col] == '*':
        return

    # Check if current position is marked as 'Visited'
    if lab[row][col] == 'v':
        return

    path.append(direction)

    # Check if current position is 'EXIT'
    if lab[row][col] == 'e':
        result.append(''.join(path))
    else:
        # Marked current position as 'Visited'
        lab[row][col] = 'v'

        # Call function in four directions
        find_all_paths(row, col + 1, lab, 'R', path, result)
        find_all_paths(row, col - 1, lab, 'L', path, result)
        find_all_paths(row + 1, col, lab, 'D', path, result)
        find_all_paths(row - 1, col, lab, 'U', path, result)
        lab[row][col] = '-'

    path.pop()


def get_all_paths(lab):
    result = []
    find_all_paths(0, 0, [list(row) for row in lab], '', [], result)
    return result


def main():
    rows = int(input())
    cols = int(input())

    matrix = []

    for _ in range(rows):
        matrix.append(input())

    for path in get_all_paths(matrix):
        print(path)


if __name__ == '__main__':
    main()
