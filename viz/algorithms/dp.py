from viz.steps import CELL, DONE, PATH, Step


def copy_table(table):
    """Copy the outer list and every row."""
    return [row[:] for row in table]


def lcs(first, second):
    """Yield the steps of the longest common subsequence.

    The table has len(first) + 1 rows and len(second) + 1 columns.
    First a CELL step for each cell (row, col) from row 1 and col 1.
    info is the cells that it reads from. Then a PATH step for each cell
    on the way back, and DONE with the answer in info.
    """
    rows = len(first) + 1
    cols = len(second) + 1
    table = [[0] * cols for _ in range(rows)]

    for row in range(1, rows):
        for col in range(1, cols):
            if first[row - 1] == second[col - 1]:
                reads = ((row - 1, col - 1),)
                table[row][col] = table[row - 1][col - 1] + 1
            else:
                reads = ((row - 1, col), (row, col - 1))
                table[row][col] = max(table[row - 1][col],
                                      table[row][col - 1])
            yield Step(CELL, (row, col), copy_table(table), reads)

    # The way back, from the bottom right corner.
    row, col = rows - 1, cols - 1
    path = [(row, col)]
    letters = []
    yield Step(PATH, (row, col), copy_table(table), tuple(path))
    while row > 0 and col > 0:
        if first[row - 1] == second[col - 1]:
            letters.append(first[row - 1])
            row -= 1
            col -= 1
        elif table[row - 1][col] > table[row][col - 1]:
            row -= 1
        else:
            col -= 1
        path.append((row, col))
        yield Step(PATH, (row, col), copy_table(table), tuple(path))

    answer = ''.join(reversed(letters))
    yield Step(DONE, (), copy_table(table), answer)


def lcs_answer(steps):
    """The answer string from a list of steps."""
    return steps[-1].info


def edit_distance(first, second):
    """Yield the steps of the minimum edit distance. All costs are 1.

    The table has len(first) + 1 rows and len(second) + 1 columns.
    First a CELL step for each cell of the top row and the left column,
    then for each other cell. info is the cells that it reads from.
    Then a PATH step for each cell on the way back to (0, 0),
    and DONE with the distance in info.
    """
    rows = len(first) + 1
    cols = len(second) + 1
    table = [[0] * cols for _ in range(rows)]

    for col in range(1, cols):
        table[0][col] = table[0][col - 1] + 1
        yield Step(CELL, (0, col), copy_table(table), ((0, col - 1),))

    for row in range(1, rows):
        table[row][0] = table[row - 1][0] + 1
        yield Step(CELL, (row, 0), copy_table(table), ((row - 1, 0),))

    for row in range(1, rows):
        for col in range(1, cols):
            if first[row - 1] == second[col - 1]:
                reads = ((row - 1, col - 1),)
                table[row][col] = table[row - 1][col - 1]
            else:
                reads = ((row, col - 1), (row - 1, col), (row - 1, col - 1))
                table[row][col] = 1 + min(table[row][col - 1],
                                          table[row - 1][col],
                                          table[row - 1][col - 1])
            yield Step(CELL, (row, col), copy_table(table), reads)

    # The way back, from the bottom right corner to the top left corner.
    row, col = rows - 1, cols - 1
    path = [(row, col)]
    yield Step(PATH, (row, col), copy_table(table), tuple(path))
    while row > 0 or col > 0:
        if row == 0:
            col -= 1
        elif col == 0:
            row -= 1
        elif first[row - 1] == second[col - 1]:
            row -= 1
            col -= 1
        else:
            best = min(table[row - 1][col - 1], table[row][col - 1],
                       table[row - 1][col])
            if table[row - 1][col - 1] == best:
                row -= 1
                col -= 1
            elif table[row][col - 1] == best:
                col -= 1
            else:
                row -= 1
        path.append((row, col))
        yield Step(PATH, (row, col), copy_table(table), tuple(path))

    yield Step(DONE, (), copy_table(table), table[rows - 1][cols - 1])


def edit_distance_answer(steps):
    """The distance from a list of steps."""
    return steps[-1].info


def move_down_right(grid):
    """Yield the steps of the best sum from the top left to the bottom right.

    You can only move down or right. The table has the same size as the grid.
    A CELL step for each cell, row by row. info is the cells that it reads
    from. Then a PATH step for each cell on the way back, and DONE with the
    best sum in info. An empty grid gives only DONE with 0.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if cols == 0:
        yield Step(DONE, (), [], 0)
        return

    table = [[0] * cols for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if row == 0 and col == 0:
                reads = ()
                table[row][col] = grid[row][col]
            elif row == 0:
                reads = ((row, col - 1),)
                table[row][col] = table[row][col - 1] + grid[row][col]
            elif col == 0:
                reads = ((row - 1, col),)
                table[row][col] = table[row - 1][col] + grid[row][col]
            else:
                reads = ((row - 1, col), (row, col - 1))
                table[row][col] = (max(table[row - 1][col],
                                       table[row][col - 1]) + grid[row][col])
            yield Step(CELL, (row, col), copy_table(table), reads)

    # The way back. On a tie it goes left, like the script does.
    row, col = rows - 1, cols - 1
    path = [(row, col)]
    yield Step(PATH, (row, col), copy_table(table), tuple(path))
    while row > 0 or col > 0:
        if row == 0:
            col -= 1
        elif col == 0:
            row -= 1
        elif table[row][col - 1] >= table[row - 1][col]:
            col -= 1
        else:
            row -= 1
        path.append((row, col))
        yield Step(PATH, (row, col), copy_table(table), tuple(path))

    yield Step(DONE, (), copy_table(table), table[rows - 1][cols - 1])


def best_path_cells(steps):
    """The path from the top left cell as a list of [row, col] cells."""
    paths = [s for s in steps if s.kind == PATH]
    if not paths:
        return []
    return [list(cell) for cell in reversed(paths[-1].info)]


def best_sum(steps):
    """The best sum from a list of steps."""
    return steps[-1].info
