import pytest

FOLDER = 'Graph Theory, Traversal and Topological Sorting - Exercise'


@pytest.fixture(scope='module')
def areas_mod(load):
    return load(FOLDER, '01_areas_in_matrix.py')


@pytest.fixture(scope='module')
def cycles_mod(load):
    return load(FOLDER, '02_cycles_in_graph.py')


@pytest.fixture(scope='module')
def salaries_mod(load):
    return load(FOLDER, '03_salaries.py')


@pytest.fixture(scope='module')
def break_mod(load):
    return load(FOLDER, '04_break_cycles.py')


@pytest.fixture(scope='module')
def roads_mod(load):
    return load(FOLDER, '05_road_reconstruction.py')


def make_matrix(lines):
    return [list(line) for line in lines]


def test_areas_in_matrix(areas_mod):
    matrix = make_matrix(['aab', 'abb'])
    assert areas_mod.count_areas(2, 3, matrix) == (2, {'a': 1, 'b': 1})


def test_areas_same_letter_apart(areas_mod):
    matrix = make_matrix(['aba'])
    assert areas_mod.count_areas(1, 3, matrix) == (3, {'a': 2, 'b': 1})


def test_areas_one_cell(areas_mod):
    assert areas_mod.count_areas(1, 1, make_matrix(['a'])) == (1, {'a': 1})


def test_areas_all_same_letter(areas_mod):
    matrix = make_matrix(['aaa', 'aaa'])
    assert areas_mod.count_areas(2, 3, matrix) == (1, {'a': 1})


def test_acyclic_graph(cycles_mod):
    assert cycles_mod.is_acyclic({'A': ['B'], 'B': ['C'], 'C': []}) is True


def test_acyclic_diamond_is_not_a_cycle(cycles_mod):
    graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
    assert cycles_mod.is_acyclic(graph) is True


def test_cycle(cycles_mod):
    assert cycles_mod.is_acyclic({'A': ['B'], 'B': ['A']}) is False
    assert cycles_mod.is_acyclic({'A': ['B'], 'B': ['C'], 'C': ['A']}) is False


def test_self_loop(cycles_mod):
    assert cycles_mod.is_acyclic({'A': ['A']}) is False


def test_empty_graph_is_acyclic(cycles_mod):
    assert cycles_mod.is_acyclic({}) is True


def test_salaries(salaries_mod):
    assert salaries_mod.total_salaries(['NNYN', 'NNYN', 'NNNN', 'NYYN']) == 5


def test_salaries_one_employee(salaries_mod):
    assert salaries_mod.total_salaries(['N']) == 1


def test_salaries_no_managers(salaries_mod):
    assert salaries_mod.total_salaries(['NNN', 'NNN', 'NNN']) == 3


def test_break_cycles_triangle(break_mod):
    graph = {'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B']}
    assert len(break_mod.find_edges_to_remove(graph)) == 1


def test_break_cycles_tree_needs_nothing(break_mod):
    assert break_mod.find_edges_to_remove({'A': ['B'], 'B': ['A']}) == []


def test_break_cycles_leaves_a_graph_without_cycles(break_mod):
    graph = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'C', 'D'],
        'C': ['A', 'B', 'D'],
        'D': ['A', 'B', 'C'],
    }
    removed = break_mod.find_edges_to_remove(graph)

    # K4 has 6 edges. A tree on 4 nodes has 3 edges.
    assert len(removed) == 3


def test_important_streets_chain(roads_mod):
    assert roads_mod.find_important_streets(3, [(0, 1), (1, 2)]) == [(0, 1), (1, 2)]


def test_important_streets_triangle(roads_mod):
    assert roads_mod.find_important_streets(3, [(0, 1), (1, 2), (0, 2)]) == []


def test_important_streets_cycle_with_tail(roads_mod):
    streets = [(0, 1), (1, 2), (2, 0), (2, 3)]
    assert roads_mod.find_important_streets(4, streets) == [(2, 3)]


def test_important_streets_no_streets(roads_mod):
    assert roads_mod.find_important_streets(1, []) == []
