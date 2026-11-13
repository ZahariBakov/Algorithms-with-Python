import random
import sys
from pathlib import Path

import pytest

# Make "import viz" work. No pygame is used in this file.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from viz.algorithms.searching import binary_search, result_index  # noqa: E402
from viz.steps import DONE, NOT_FOUND, RANGE  # noqa: E402


def run(values, target):
    return list(binary_search(values, target))


def test_result_matches_list_index():
    rng = random.Random(1)
    for _ in range(50):
        values = sorted(rng.sample(range(-50, 50), rng.randint(1, 30)))
        for target in values:
            steps = run(values, target)
            assert result_index(steps) == values.index(target)


def test_missing_target_gives_minus_one():
    rng = random.Random(2)
    for _ in range(50):
        values = sorted(rng.sample(range(0, 100, 2), rng.randint(0, 20)))
        for target in (-1, 1, 51, 101):
            if target in values:
                continue
            steps = run(values, target)
            assert result_index(steps) == -1
            assert steps[-1].kind == NOT_FOUND


def test_empty_list():
    steps = run([], 5)
    assert [s.kind for s in steps] == [NOT_FOUND]
    assert result_index(steps) == -1


def test_one_item_list():
    found = run([7], 7)
    assert [s.kind for s in found] == [RANGE, DONE]
    assert result_index(found) == 0
    assert result_index(run([7], 3)) == -1
    assert result_index(run([7], 9)) == -1


def test_range_steps_show_left_mid_right():
    steps = run([1, 3, 5, 7, 9], 9)
    assert steps[0].kind == RANGE
    assert steps[0].indices == (0, 2, 4)
    for step in steps[:-1]:
        left, mid, right = step.indices
        assert left <= mid <= right
    assert steps[-1].kind == DONE
    assert steps[-1].indices == (4,)


def test_data_is_not_changed():
    values = [1, 2, 3, 4]
    steps = run(values, 3)
    assert values == [1, 2, 3, 4]
    assert all(step.data == [1, 2, 3, 4] for step in steps)


def test_generator_ends():
    generator = binary_search([1, 2, 3], 2)
    for _ in generator:
        pass
    with pytest.raises(StopIteration):
        next(generator)
