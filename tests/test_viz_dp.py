import random
import sys
from pathlib import Path

import pytest

# Make "import viz" work. No pygame is used in this file.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from viz.algorithms.dp import lcs, lcs_answer  # noqa: E402
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
