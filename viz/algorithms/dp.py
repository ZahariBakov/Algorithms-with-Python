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
