import random
import sys
from pathlib import Path

import pytest

# Make "import viz" work. No pygame is used in this file.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from viz.algorithms.dp import (  # noqa: E402
    best_path_cells,
    best_sum,
    edit_distance,
    edit_distance_answer,
    lcs,
    lcs_answer,
    move_down_right,
)
from viz.steps import CELL, DONE, PATH  # noqa: E402

FOLDER = 'Dynamic Programming - Lab'
FILE = '03_longest_common_subsequence.py'

WORDS = ['algorithm', 'python', 'computer', 'keyboard', 'subsequence',
         'sequence', 'recursion', 'iteration', 'a', 'abc', 'aaa']


@pytest.fixture(scope='module')
def reference(load):
    return load(FOLDER, FILE).longest_common_subsequence


def is_subsequence(small, big):
    items = iter(big)
    return all(letter in items for letter in small)


def run(first, second):
    return list(lcs(first, second))


def test_answer_has_the_same_length_as_the_script(reference):
    for first in WORDS:
        for second in WORDS:
            length, expected = reference(first, second)
            answer = lcs_answer(run(first, second))
            assert len(answer) == length
            assert answer == expected


def test_random_strings(reference):
    rng = random.Random(3)
    for _ in range(100):
        first = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 10)))
        second = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 10)))
        answer = lcs_answer(run(first, second))
        assert len(answer) == reference(first, second)[0]
        assert is_subsequence(answer, first)
        assert is_subsequence(answer, second)


@pytest.mark.parametrize('first, second', [('', ''), ('abc', ''), ('', 'abc')])
def test_empty_strings(first, second):
    steps = run(first, second)
    assert steps[-1].kind == DONE
    assert lcs_answer(steps) == ''
    assert not [s for s in steps if s.kind == CELL]


def test_the_generator_ends():
    generator = lcs('python', 'typhon')
    steps = list(generator)
    assert steps[-1].kind == DONE
    assert next(generator, None) is None


def test_cell_steps_read_from_the_right_cells():
    steps = run('ab', 'ba')
    cells = [s for s in steps if s.kind == CELL]
    assert [s.indices for s in cells] == [(1, 1), (1, 2), (2, 1), (2, 2)]
    # 'a' and 'b' are different: it reads the cell above and the cell on the left.
    assert cells[0].info == ((0, 1), (1, 0))
    # 'a' and 'a' are the same: it reads the cell on the diagonal.
    assert cells[1].info == ((0, 1),)


def test_path_goes_from_the_corner_to_the_edge():
    steps = run('abcd', 'xbd')
    path_steps = [s for s in steps if s.kind == PATH]
    assert path_steps[0].info == ((4, 3),)
    last = path_steps[-1].info[-1]
    assert last[0] == 0 or last[1] == 0


def test_steps_have_their_own_copy_of_the_table():
    steps = run('abc', 'abc')
    first_cell = steps[0]
    final = steps[-1].data
    # Early in the work, later cells are still 0.
    assert first_cell.data != final
    assert first_cell.data[3][3] == 0
    assert final[3][3] == 3
    # Every row is a copy, so no two steps share a row.
    assert first_cell.data[1] is not steps[1].data[1]
    assert first_cell.data[1] is not final[1]


def assert_every_row_is_a_copy(steps):
    ids = [id(row) for s in steps for row in s.data]
    assert len(set(ids)) == len(ids)
    # The first picture is not changed by later work.
    tables = [s for s in steps if s.data]
    assert tables[0].data != tables[-1].data


# Edit distance (key 9)

EDIT_FOLDER = 'Dynamic Programming - Exercise'
EDIT_FILE = '04_minimum_edit_distance.py'


@pytest.fixture(scope='module')
def edit_reference(load):
    return load(EDIT_FOLDER, EDIT_FILE).min_edit_distance


def test_edit_distance_is_the_same_as_the_script(edit_reference):
    for first in WORDS:
        for second in WORDS:
            steps = list(edit_distance(first, second))
            expected = edit_reference(1, 1, 1, first, second)
            assert edit_distance_answer(steps) == expected


def test_edit_distance_random_strings(edit_reference):
    rng = random.Random(5)
    for _ in range(100):
        first = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 8)))
        second = ''.join(rng.choice('abc') for _ in range(rng.randint(0, 8)))
        steps = list(edit_distance(first, second))
        assert edit_distance_answer(steps) == edit_reference(
            1, 1, 1, first, second)


@pytest.mark.parametrize('first, second, expected', [
    ('', '', 0), ('abc', '', 3), ('', 'abc', 3), ('a', 'a', 0)])
def test_edit_distance_small_inputs(first, second, expected):
    steps = list(edit_distance(first, second))
    assert steps[-1].kind == DONE
    assert edit_distance_answer(steps) == expected
    # The path always ends in the top left cell.
    paths = [s for s in steps if s.kind == PATH]
    assert paths[-1].info[-1] == (0, 0)


def test_edit_distance_cells_and_path():
    steps = list(edit_distance('ab', 'ba'))
    cells = [s for s in steps if s.kind == CELL]
    assert [s.indices for s in cells] == [
        (0, 1), (0, 2), (1, 0), (2, 0), (1, 1), (1, 2), (2, 1), (2, 2)]
    # Different letters: it reads left, up and the diagonal.
    assert cells[4].info == ((1, 0), (0, 1), (0, 0))
    # Same letters: it reads the diagonal only.
    assert cells[5].info == ((0, 1),)
    path = [s for s in steps if s.kind == PATH][-1].info
    assert path[0] == (2, 2)
    assert path[-1] == (0, 0)


def test_edit_distance_steps_copy_every_row():
    assert_every_row_is_a_copy(list(edit_distance('abc', 'abd')))


# Move down right (key 0)

GRID_FOLDER = 'Dynamic Programming - Lab'
GRID_FILE = '02_move_down_right.py'


@pytest.fixture(scope='module')
def grid_reference(load):
    return load(GRID_FOLDER, GRID_FILE).best_path


def grid_total(grid, cells):
    return sum(grid[row][col] for row, col in cells)


def test_move_down_right_path_is_the_same_as_the_script(grid_reference):
    rng = random.Random(7)
    for _ in range(100):
        rows = rng.randint(1, 6)
        cols = rng.randint(1, 6)
        grid = [[rng.randint(1, 9) for _ in range(cols)] for _ in range(rows)]
        steps = list(move_down_right(grid))
        expected = grid_reference(rows, cols, grid)
        assert best_path_cells(steps) == expected
        assert best_sum(steps) == grid_total(grid, expected)


@pytest.mark.parametrize('grid', [[[5]], [[1, 2, 3]], [[1], [2], [3]]])
def test_move_down_right_small_grids(grid, grid_reference):
    steps = list(move_down_right(grid))
    assert steps[-1].kind == DONE
    cells = best_path_cells(steps)
    assert cells == grid_reference(len(grid), len(grid[0]), grid)
    assert best_sum(steps) == sum(sum(row) for row in grid)


@pytest.mark.parametrize('grid', [[], [[]]])
def test_move_down_right_empty_grid(grid):
    steps = list(move_down_right(grid))
    assert [s.kind for s in steps] == [DONE]
    assert best_sum(steps) == 0
    assert best_path_cells(steps) == []


def test_move_down_right_cells_and_path():
    steps = list(move_down_right([[1, 2], [3, 4]]))
    cells = [s for s in steps if s.kind == CELL]
    assert [s.indices for s in cells] == [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert [s.info for s in cells] == [
        (), ((0, 0),), ((0, 0),), ((0, 1), (1, 0))]
    assert steps[-1].data == [[1, 3], [4, 8]]
    assert best_sum(steps) == 8
    assert best_path_cells(steps) == [[0, 0], [1, 0], [1, 1]]


def test_move_down_right_steps_copy_every_row():
    assert_every_row_is_a_copy(list(move_down_right([[1, 2, 3], [4, 5, 6]])))
