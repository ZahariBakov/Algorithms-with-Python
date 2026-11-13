import random

import pytest

FOLDER = 'Searching and Sorting Algorithms - Lab'

SORTS = [
    ('02_selection_sort.py', lambda mod, nums: mod.selection_sort(nums)),
    ('03_bubble_sort.py', lambda mod, nums: mod.bubble_sort(nums)),
    ('04_insertion_sort.py', lambda mod, nums: mod.insertion_sort(nums)),
    ('05_quicksort.py', lambda mod, nums: (mod.quick_sort(0, len(nums) - 1, nums), nums)[1]),
    ('06_merge_sort.py', lambda mod, nums: mod.merge_sort(nums)),
]

CASES = [
    [],
    [1],
    [2, 1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 1, 2, 3, 1, 2],
    [7, 7, 7, 7],
    [-3, 0, -10, 5, 2],
    [10, 9, 1, 8, 2, 7, 3, 6, 4, 5],
]


@pytest.fixture(scope='module')
def search_mod(load):
    return load(FOLDER, '01_binary_search.py')


@pytest.mark.parametrize('filename, sort', SORTS, ids=[name for name, _ in SORTS])
@pytest.mark.parametrize('nums', CASES)
def test_sort_matches_sorted(load, filename, sort, nums):
    mod = load(FOLDER, filename)
    assert sort(mod, list(nums)) == sorted(nums)


@pytest.mark.parametrize('filename, sort', SORTS, ids=[name for name, _ in SORTS])
def test_sort_random_lists(load, filename, sort):
    mod = load(FOLDER, filename)
    rng = random.Random(12345)

    for _ in range(50):
        nums = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
        assert sort(mod, list(nums)) == sorted(nums)


@pytest.mark.parametrize('target, expected', [(1, 0), (5, 2), (9, 4), (3, 1), (7, 3)])
def test_binary_search_found(search_mod, target, expected):
    nums = [1, 3, 5, 7, 9]
    assert search_mod.binary_search(0, len(nums) - 1, nums, target) == expected


@pytest.mark.parametrize('target', [0, 4, 10])
def test_binary_search_not_found(search_mod, target):
    nums = [1, 3, 5, 7, 9]
    assert search_mod.binary_search(0, len(nums) - 1, nums, target) == -1


def test_binary_search_empty(search_mod):
    assert search_mod.binary_search(0, -1, [], 5) == -1


def test_binary_search_one_item(search_mod):
    assert search_mod.binary_search(0, 0, [5], 5) == 0
    assert search_mod.binary_search(0, 0, [5], 6) == -1
