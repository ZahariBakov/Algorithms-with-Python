# class Area:
#     def __init__(self, row, col, size):
#         self.row = row
#         self.col = col
#         self.size = size


def explore_area(row, col, matrix):
    if row < 0 or col < 0 or row >= len(matrix) or col >= len(matrix[0]):
        return 0

    if matrix[row][col] != '-':
        return 0

    matrix[row][col] = 'v'
    result = 1

    result += explore_area(row - 1, col, matrix)
    result += explore_area(row + 1, col, matrix)
    result += explore_area(row, col - 1, matrix)
    result += explore_area(row, col + 1, matrix)

    return result


def find_areas(rows, cols, matrix):
    areas = []

    for row in range(rows):
        for col in range(cols):
            size = explore_area(row, col, matrix)
            if size == 0:
                continue
            # areas.append(Area(row, col, size))
            areas.append((row, col, size))

    return sorted(areas, key=lambda x: -x[2])


def main():
    rows = int(input())
    cols = int(input())

    matrix = []

    for _ in range(rows):
        matrix.append(list(input()))

    areas = find_areas(rows, cols, matrix)

    print(f'Total areas found: {len(areas)}')
    # for idx, area in enumerate(sorted(areas, key=lambda x: -x.size)):
    #     print(f'Area #{idx + 1} at ({area.row}, {area.col}), size: {area.size}')

    for idx, (row, col, size) in enumerate(areas):
        print(f'Area #{idx + 1} at ({row}, {col}), size: {size}')


if __name__ == '__main__':
    main()
