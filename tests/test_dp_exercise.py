import pytest

FOLDER = 'Dynamic Programming - Exercise'


@pytest.fixture(scope='module')
def binom_mod(load):
    return load(FOLDER, '01_binomial_coefficients.py')


@pytest.fixture(scope='module')
def diff_mod(load):
    return load(FOLDER, '02_word_differences.py')


@pytest.fixture(scope='module')
def cables_mod(load):
    return load(FOLDER, '03_connecting_cables.py')


@pytest.fixture(scope='module')
def edit_mod(load):
    return load(FOLDER, '04_minimum_edit_distance.py')


@pytest.fixture(scope='module')
def chain_mod(load):
    return load(FOLDER, '05_longest_string_chain.py')


@pytest.fixture(scope='module')
def zigzag_mod(load):
    return load(FOLDER, '06_longest_zigzag_subsequence.py')


@pytest.mark.parametrize('n, k, expected', [
    (0, 0, 1),
    (4, 0, 1),
    (4, 4, 1),
    (5, 2, 10),
    (10, 5, 252),
    (3, 5, 0),
])
def test_binomial(binom_mod, n, k, expected):
    assert binom_mod.calc_binom(n, k, {}) == expected


@pytest.mark.parametrize('first, second, expected', [
    ('abc', 'abc', 0),
    ('abc', 'abd', 2),
    ('sea', 'eat', 2),
    ('', 'abc', 3),
    ('abc', '', 3),
    ('', '', 0),
    ('abc', 'xyz', 6),
])
def test_word_differences(diff_mod, first, second, expected):
    assert diff_mod.word_differences(first, second) == expected


@pytest.mark.parametrize('cables, expected', [
    ([1, 2, 3], 3),
    ([3, 2, 1], 1),
    ([2, 1, 3], 2),
    ([1], 1),
    ([], 0),
])
def test_connecting_cables(cables_mod, cables, expected):
    assert cables_mod.max_connected_pairs(cables) == expected


@pytest.mark.parametrize('costs, first, second, expected', [
    ((1, 1, 1), 'kitten', 'sitting', 3),
    ((1, 1, 1), 'abc', 'abc', 0),
    ((1, 2, 3), '', 'abc', 6),
    ((1, 2, 3), 'abc', '', 9),
    ((5, 1, 1), 'a', 'b', 2),
    ((1, 1, 1), '', '', 0),
])
def test_min_edit_distance(edit_mod, costs, first, second, expected):
    replace_cost, insert_cost, delete_cost = costs
    result = edit_mod.min_edit_distance(replace_cost, insert_cost, delete_cost, first, second)
    assert result == expected


def test_string_chain(chain_mod):
    assert chain_mod.longest_string_chain(['a', 'ab', 'abc']) == ['a', 'ab', 'abc']


def test_string_chain_unsorted_input(chain_mod):
    assert chain_mod.longest_string_chain(['abcd', 'a', 'ab', 'abc']) == ['a', 'ab', 'abc']


def test_string_chain_one_word(chain_mod):
    assert chain_mod.longest_string_chain(['a']) == ['a']


def test_zigzag(zigzag_mod):
    assert zigzag_mod.longest_zigzag_subsequence([1, 2, 1, 2]) == [1, 2, 1, 2]


def test_zigzag_one_item(zigzag_mod):
    assert zigzag_mod.longest_zigzag_subsequence([5]) == [5]


def test_zigzag_increasing_numbers(zigzag_mod):
    assert zigzag_mod.longest_zigzag_subsequence([1, 2, 3]) == [1, 2]


def test_zigzag_result_alternates(zigzag_mod):
    nums = [1, 7, 4, 9, 2, 5]
    result = zigzag_mod.longest_zigzag_subsequence(nums)

    assert len(result) == 6

    for idx in range(1, len(result) - 1):
        assert (result[idx] - result[idx - 1]) * (result[idx + 1] - result[idx]) < 0
