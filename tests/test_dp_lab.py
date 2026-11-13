import pytest

FOLDER = 'Dynamic Programming - Lab'


@pytest.fixture(scope='module')
def fib_mod(load):
    return load(FOLDER, '01_fibonacci.py')


@pytest.fixture(scope='module')
def grid_mod(load):
    return load(FOLDER, '02_move_down_right.py')


@pytest.fixture(scope='module')
def lcs_mod(load):
    return load(FOLDER, '03_longest_common_subsequence.py')


@pytest.fixture(scope='module')
def lis_mod(load):
    return load(FOLDER, '04_longest_increasing_subsequence.py')


@pytest.mark.parametrize('n, expected', [
    (1, 1),
    (2, 1),
    (3, 2),
    (10, 55),
    (50, 12586269025),
])
def test_fibonacci(fib_mod, n, expected):
    assert fib_mod.calc_fib(n, {}) == expected


def test_best_path_two_by_two(grid_mod):
    matrix = [[1, 2], [3, 4]]
    assert grid_mod.best_path(2, 2, matrix) == [[0, 0], [1, 0], [1, 1]]


def test_best_path_one_cell(grid_mod):
    assert grid_mod.best_path(1, 1, [[7]]) == [[0, 0]]


def test_best_path_one_row_and_one_column(grid_mod):
    assert grid_mod.best_path(1, 3, [[1, 2, 3]]) == [[0, 0], [0, 1], [0, 2]]
    assert grid_mod.best_path(3, 1, [[1], [2], [3]]) == [[0, 0], [1, 0], [2, 0]]


def test_best_path_takes_the_bigger_cells(grid_mod):
    matrix = [
        [1, 1, 1],
        [1, 9, 1],
        [1, 1, 1],
    ]
    path = grid_mod.best_path(3, 3, matrix)
    assert [1, 1] in path
    assert path[0] == [0, 0]
    assert path[-1] == [2, 2]
    assert len(path) == 5


@pytest.mark.parametrize('first, second, length, text', [
    ('abc', 'abc', 3, 'abc'),
    ('abcde', 'ace', 3, 'ace'),
    ('abc', 'def', 0, ''),
    ('', 'abc', 0, ''),
    ('abc', '', 0, ''),
    ('', '', 0, ''),
    ('a', 'a', 1, 'a'),
])
def test_longest_common_subsequence(lcs_mod, first, second, length, text):
    assert lcs_mod.longest_common_subsequence(first, second) == (length, text)


def test_lis_increasing(lis_mod):
    assert lis_mod.longest_increasing_subsequence([1, 2, 3]) == (3, [1, 2, 3])


def test_lis_decreasing(lis_mod):
    size, result = lis_mod.longest_increasing_subsequence([3, 2, 1])
    assert size == 1
    assert len(result) == 1


def test_lis_one_item(lis_mod):
    assert lis_mod.longest_increasing_subsequence([5]) == (1, [5])


def test_lis_mixed(lis_mod):
    assert lis_mod.longest_increasing_subsequence([1, 3, 2, 4]) == (3, [1, 3, 4])


def test_lis_equal_numbers_are_not_increasing(lis_mod):
    size, result = lis_mod.longest_increasing_subsequence([4, 4, 4])
    assert size == 1
    assert len(result) == 1
