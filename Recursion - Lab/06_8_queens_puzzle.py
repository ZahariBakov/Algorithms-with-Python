def format_board(board):
    return [' '.join(row) for row in board]


def can_place_queen(row, col, rows, cols, left_diagonals, right_diagonals):
    if row in rows:
        return False
    if col in cols:
        return False
    if (row - col) in left_diagonals:
        return False
    if (row + col) in right_diagonals:
        return False

    return True


def set_queen(row, col, board, rows, cols, left_diagonals, right_diagonals):
    board[row][col] = '*'
    rows.add(row)
    cols.add(col)
    left_diagonals.add(row - col)
    right_diagonals.add(row + col)


def remove_queen(row, col, board, rows, cols, left_diagonals, right_diagonals):
    board[row][col] = '-'
    rows.remove(row)
    cols.remove(col)
    left_diagonals.remove(row - col)
    right_diagonals.remove(row + col)


def put_queens(row, n, board, rows, cols, left_diagonals, right_diagonals, solutions):
    if row == n:
        solutions.append(format_board(board))
        return

    for col in range(n):
        if can_place_queen(row, col, rows, cols, left_diagonals, right_diagonals):
            set_queen(row, col, board, rows, cols, left_diagonals, right_diagonals)
            put_queens(row + 1, n, board, rows, cols, left_diagonals, right_diagonals, solutions)
            remove_queen(row, col, board, rows, cols, left_diagonals, right_diagonals)


def solve_queens(n):
    board = []
    [board.append(['-'] * n) for _ in range(n)]

    solutions = []
    put_queens(0, n, board, set(), set(), set(), set(), solutions)
    return solutions


def main():
    n = 8

    for solution in solve_queens(n):
        for line in solution:
            print(line)
        print()


if __name__ == '__main__':
    main()
