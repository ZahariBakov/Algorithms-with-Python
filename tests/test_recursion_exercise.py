import pytest

FOLDER = 'Recursion - Exercise'


@pytest.fixture(scope='module')
def reverse_mod(load):
    return load(FOLDER, '01_reverse_array.py')


@pytest.fixture(scope='module')
def loops_mod(load):
    return load(FOLDER, '02_nested_loops.py')


@pytest.fixture(scope='module')
def paths_mod(load):
    return load(FOLDER, '03_move_down_right.py')


@pytest.fixture(scope='module')
def areas_mod(load):
    return load(FOLDER, '04_connected_areas_in_matrix.py')


@pytest.fixture(scope='module')
def cruncher_mod(load):
    return load(FOLDER, '05_word_cruncher.py')


@pytest.mark.parametrize('items', [
    [],
    ['1'],
    ['1', '2'],
    ['1', '2', '3'],
    ['a', 'b', 'c', 'd'],
    ['a', 'b', 'c', 'd', 'e'],
])
def test_reverse_array(reverse_mod, items):
    array = list(items)
    reverse_mod.reverse_aray(0, array)
    assert array == items[::-1]


def test_nested_loops(loops_mod):
    assert loops_mod.get_nested_loops(2) == ['1 1', '1 2', '2 1', '2 2']
    assert len(loops_mod.get_nested_loops(3)) == 27


def test_nested_loops_edge(loops_mod):
    assert loops_mod.get_nested_loops(1) == ['1']
    assert loops_mod.get_nested_loops(0) == ['']


@pytest.mark.parametrize('rows, cols, expected', [
    (1, 1, 1),
    (1, 5, 1),
    (5, 1, 1),
    (2, 2, 2),
    (3, 3, 6),
    (3, 4, 10),
])
def test_count_all_paths(paths_mod, rows, cols, expected):
    assert paths_mod.count_all_paths(0, 0, rows, cols) == expected


def make_matrix(lines):
    return [list(line) for line in lines]


def test_areas_sorted_by_size(areas_mod):
    lines = ['-*-', '*--']
    result = areas_mod.find_areas(2, 3, make_matrix(lines))
    assert result == [(0, 2, 3), (0, 0, 1)]


def test_areas_equal_size_keep_order(areas_mod):
    lines = ['-*-', '-*-']
    result = areas_mod.find_areas(2, 3, make_matrix(lines))
    assert result == [(0, 0, 2), (0, 2, 2)]


def test_areas_one_cell(areas_mod):
    assert areas_mod.find_areas(1, 1, make_matrix(['-'])) == [(0, 0, 1)]


def test_areas_no_areas(areas_mod):
    assert areas_mod.find_areas(2, 2, make_matrix(['**', '**'])) == []


def test_word_cruncher_simple(cruncher_mod):
    assert cruncher_mod.crunch_words(['ab', 'cd'], 'abcd') == ['ab cd']


def test_word_cruncher_many_solutions(cruncher_mod):
    result = cruncher_mod.crunch_words(['a', 'b', 'ab'], 'ab')
    assert result == ['a b', 'ab']


def test_word_cruncher_no_solution(cruncher_mod):
    assert cruncher_mod.crunch_words(['ab'], 'abc') == []
    assert cruncher_mod.crunch_words(['x', 'y'], 'abc') == []


def test_word_cruncher_word_used_by_count(cruncher_mod):
    assert cruncher_mod.crunch_words(['a'], 'aa') == []
    assert cruncher_mod.crunch_words(['a', 'a'], 'aa') == ['a a']
