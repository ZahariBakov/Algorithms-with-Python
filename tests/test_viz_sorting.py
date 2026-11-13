import random
import sys
from pathlib import Path

import pytest

# Make "import viz" work. No pygame is used in this file.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from viz.algorithms.sorting import (  # noqa: E402
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)
from viz.steps import DONE, WRITE, Step  # noqa: E402

# Sorts that change the list by swapping two items.
SWAP_ALGORITHMS = [bubble_sort, selection_sort, insertion_sort, quick_sort, heap_sort]
ALGORITHMS = SWAP_ALGORITHMS + [merge_sort]


def run(algorithm, values):
    return list(algorithm(values))


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_data_is_sorted_after_last_step(algorithm):
    rng = random.Random(1)
    for _ in range(30):
        original = [rng.randint(-20, 20) for _ in range(rng.randint(0, 15))]
        steps = run(algorithm, original)
        assert steps[-1].data == sorted(original)


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_generator_ends(algorithm):
    generator = algorithm([3, 1, 2])
    for _ in generator:
        pass
    with pytest.raises(StopIteration):
        next(generator)


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_empty_list(algorithm):
    steps = run(algorithm, [])
    assert steps[-1].kind == DONE
    assert steps[-1].data == []


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_one_item(algorithm):
    steps = run(algorithm, [5])
    assert steps[-1].kind == DONE
    assert steps[-1].data == [5]


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_already_sorted_and_reversed(algorithm):
    assert run(algorithm, [1, 2, 3, 4])[-1].data == [1, 2, 3, 4]
    assert run(algorithm, [4, 3, 2, 1])[-1].data == [1, 2, 3, 4]


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_input_list_is_not_changed(algorithm):
    original = [3, 1, 2]
    run(algorithm, original)
    assert original == [3, 1, 2]


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_steps_are_valid_and_data_is_a_copy(algorithm):
    steps = run(algorithm, [4, 2, 3, 1])
    assert all(isinstance(step, Step) for step in steps)
    assert steps[-1].kind == DONE
    assert [s for s in steps[:-1] if s.kind == DONE] == []
    # Every step has its own list.
    assert len({id(step.data) for step in steps}) == len(steps)
    # Old steps are not changed by later steps.
    assert steps[0].data == [4, 2, 3, 1]


@pytest.mark.parametrize('algorithm', SWAP_ALGORITHMS)
def test_swap_step_changes_the_data(algorithm):
    steps = run(algorithm, [2, 1])
    swaps = [s for s in steps if s.kind == 'swap']
    assert swaps
    assert swaps[0].data == [1, 2]


def test_merge_sort_uses_write_steps_and_no_swaps():
    steps = run(merge_sort, [2, 1])
    assert [s.kind for s in steps if s.kind == 'swap'] == []
    writes = [s for s in steps if s.kind == WRITE]
    assert len(writes) == 2
    assert writes[0].indices == (0,)
    assert writes[-1].data == [1, 2]


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_duplicates(algorithm):
    original = [3, 1, 3, 2, 1, 3, 2]
    assert run(algorithm, original)[-1].data == sorted(original)


@pytest.mark.parametrize('algorithm', SWAP_ALGORITHMS)
def test_swap_sorts_keep_the_same_items_in_every_step(algorithm):
    # Merge sort is not in this test: it writes values, so a step in the
    # middle of a merge can hold one value twice.
    original = [3, 1, 3, 2, 1, 3, 2]
    for step in run(algorithm, original):
        assert sorted(step.data) == sorted(original)


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_all_equal_items(algorithm):
    assert run(algorithm, [7, 7, 7, 7])[-1].data == [7, 7, 7, 7]


@pytest.mark.parametrize('algorithm', ALGORITHMS)
def test_indices_are_inside_the_list(algorithm):
    original = [5, 2, 9, 1, 7, 3, 8]
    for step in run(algorithm, original):
        assert all(0 <= i < len(original) for i in step.indices)
