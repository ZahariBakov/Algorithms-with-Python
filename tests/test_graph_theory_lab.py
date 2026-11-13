import pytest

FOLDER = 'Graph Theory, Traversal and Topological Sorting - Lab'


@pytest.fixture(scope='module')
def components_mod(load):
    return load(FOLDER, '01_connected_components.py')


@pytest.fixture(scope='module')
def topo_mod(load):
    return load(FOLDER, '02_topological_sorting.py')


def test_connected_components(components_mod):
    graph = [[1], [0, 2], [1], [4], [3], []]
    result = components_mod.find_components(graph)
    assert [sorted(c) for c in result] == [[0, 1, 2], [3, 4], [5]]


def test_connected_components_exact_order(components_mod):
    graph = [[1], [0, 2], [1], [4], [3], []]
    assert components_mod.find_components(graph) == [[2, 1, 0], [4, 3], [5]]


def test_connected_components_one_node(components_mod):
    assert components_mod.find_components([[]]) == [[0]]


def test_connected_components_no_nodes(components_mod):
    assert components_mod.find_components([]) == []


def test_connected_components_all_alone(components_mod):
    assert components_mod.find_components([[], [], []]) == [[0], [1], [2]]


def test_topological_sort_is_valid(topo_mod):
    graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
    result = topo_mod.topological_sort(graph)

    assert sorted(result) == ['A', 'B', 'C', 'D']

    for node, children in graph.items():
        for child in children:
            assert result.index(node) < result.index(child)


def test_topological_sort_one_node(topo_mod):
    assert topo_mod.topological_sort({'A': []}) == ['A']


def test_topological_sort_no_nodes(topo_mod):
    assert topo_mod.topological_sort({}) == []


def test_topological_sort_chain(topo_mod):
    graph = {'C': [], 'B': ['C'], 'A': ['B']}
    assert topo_mod.topological_sort(graph) == ['A', 'B', 'C']


def test_topological_sort_cycle(topo_mod):
    assert topo_mod.topological_sort({'A': ['B'], 'B': ['A']}) is None


def test_topological_sort_self_loop(topo_mod):
    assert topo_mod.topological_sort({'A': ['A']}) is None
