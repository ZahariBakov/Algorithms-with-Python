import pytest

FOLDER = 'Graphs Shortest Path and MST - Lab'

INF = float('inf')


@pytest.fixture(scope='module')
def bfs_mod(load):
    return load(FOLDER, '01_shortest_path_in_unweighted_graph.py')


@pytest.fixture(scope='module')
def dijkstra_mod(load):
    return load(FOLDER, "02_dijkstra's_algorithm.py")


@pytest.fixture(scope='module')
def bellman_mod(load):
    return load(FOLDER, '03_bellman_ford.py')


@pytest.fixture(scope='module')
def kruskal_mod(load):
    return load(FOLDER, "04_kruskal's_algorithm.py")


@pytest.fixture(scope='module')
def prim_mod(load):
    return load(FOLDER, "05_prim's_algorithm.py")


def as_sets(edges):
    return {frozenset(edge) for edge in edges}


# Unweighted graph

def test_bfs_shortest_path(bfs_mod):
    edges = [(1, 2), (2, 3), (1, 3), (3, 4)]
    assert bfs_mod.shortest_path(4, edges, 1, 4) == [1, 3, 4]


def test_bfs_same_start_and_destination(bfs_mod):
    assert bfs_mod.shortest_path(4, [(1, 2)], 1, 1) == [1]


def test_bfs_unreachable(bfs_mod):
    edges = [(1, 2), (2, 3), (3, 4)]
    assert bfs_mod.shortest_path(4, edges, 4, 1) is None


def test_bfs_no_edges(bfs_mod):
    assert bfs_mod.shortest_path(3, [], 1, 2) is None


# Dijkstra

def test_dijkstra(dijkstra_mod):
    edges = [(1, 2, 1), (2, 3, 2), (1, 3, 5)]
    assert dijkstra_mod.dijkstra(edges, 1, 3) == (3, [1, 2, 3])


def test_dijkstra_direct_edge_is_better(dijkstra_mod):
    edges = [(1, 2, 4), (2, 3, 4), (1, 3, 5)]
    assert dijkstra_mod.dijkstra(edges, 1, 3) == (5, [1, 3])


def test_dijkstra_unreachable(dijkstra_mod):
    edges = [(1, 2, 1), (2, 3, 2)]
    assert dijkstra_mod.dijkstra(edges, 3, 1) is None


def test_dijkstra_start_is_target(dijkstra_mod):
    edges = [(1, 2, 1), (2, 3, 2)]
    assert dijkstra_mod.dijkstra(edges, 2, 2) == (0, [2])


def test_dijkstra_one_edge(dijkstra_mod):
    assert dijkstra_mod.dijkstra([(0, 1, 7)], 0, 1) == (7, [0, 1])


# Bellman-Ford

def test_bellman_ford_negative_edge(bellman_mod):
    edges = [(1, 2, 4), (2, 3, -2), (1, 3, 5)]
    assert bellman_mod.bellman_ford(3, edges, 1, 3) == ('ok', [1, 2, 3], 2)


def test_bellman_ford_negative_cycle(bellman_mod):
    edges = [(1, 2, 1), (2, 3, -3), (3, 2, 1)]
    assert bellman_mod.bellman_ford(3, edges, 1, 3) == ('negative cycle', None, None)


def test_bellman_ford_no_path(bellman_mod):
    assert bellman_mod.bellman_ford(3, [(1, 2, 1)], 1, 3) == ('no path', None, None)


def test_bellman_ford_start_is_target(bellman_mod):
    assert bellman_mod.bellman_ford(3, [(1, 2, 1)], 1, 1) == ('ok', [1], 0)


# Kruskal and Prim

def test_kruskal(kruskal_mod):
    edges = [(1, 2, 1), (2, 3, 2), (1, 3, 3)]
    assert kruskal_mod.kruskal(edges) == [(1, 2), (2, 3)]


def test_kruskal_one_edge(kruskal_mod):
    assert kruskal_mod.kruskal([(0, 1, 5)]) == [(0, 1)]


def test_kruskal_two_separate_parts(kruskal_mod):
    edges = [(0, 1, 1), (2, 3, 1)]
    assert kruskal_mod.kruskal(edges) == [(0, 1), (2, 3)]


def test_kruskal_skips_the_edge_that_makes_a_cycle(kruskal_mod):
    edges = [(0, 1, 1), (1, 2, 1), (0, 2, 1)]
    assert len(kruskal_mod.kruskal(edges)) == 2


def test_prim(prim_mod):
    edges = [(1, 2, 1), (2, 3, 2), (1, 3, 3)]
    assert prim_mod.find_forest(edges) == [(1, 2), (2, 3)]


def test_prim_one_edge(prim_mod):
    assert prim_mod.find_forest([(0, 1, 5)]) == [(0, 1)]


def test_prim_two_separate_parts(prim_mod):
    edges = [(0, 1, 1), (2, 3, 1)]
    assert as_sets(prim_mod.find_forest(edges)) == {frozenset((0, 1)), frozenset((2, 3))}


def test_prim_no_edges(prim_mod):
    assert prim_mod.find_forest([]) == []


def test_prim_and_kruskal_find_the_same_tree(prim_mod, kruskal_mod):
    edges = [(0, 1, 4), (1, 2, 1), (0, 2, 3), (2, 3, 2), (1, 3, 5)]
    expected = {frozenset((0, 2)), frozenset((1, 2)), frozenset((2, 3))}

    assert as_sets(kruskal_mod.kruskal(edges)) == expected
    assert as_sets(prim_mod.find_forest(edges)) == expected
