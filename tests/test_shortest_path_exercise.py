import pytest

FOLDER = 'Graphs Shortest Path and MST - Exercise'

INF = float('inf')


@pytest.fixture(scope='module')
def distance_mod(load):
    return load(FOLDER, '01_distance_between_vertices.py')


@pytest.fixture(scope='module')
def reliable_mod(load):
    return load(FOLDER, '02_most_reliable_path.py')


@pytest.fixture(scope='module')
def tour_mod(load):
    return load(FOLDER, '03_cheap_town_tour.py')


@pytest.fixture(scope='module')
def undefined_mod(load):
    return load(FOLDER, '04_undefined.py')


@pytest.fixture(scope='module')
def network_mod(load):
    return load(FOLDER, '05_cable_network.py')


# Distance between vertices

def test_distance(distance_mod):
    graph = {1: [2], 2: [3], 3: []}
    assert distance_mod.find_distance(graph, 1, 3) == 2


def test_distance_to_itself(distance_mod):
    assert distance_mod.find_distance({1: [2], 2: []}, 1, 1) == 0


def test_distance_unreachable(distance_mod):
    graph = {1: [2], 2: [3], 3: []}
    assert distance_mod.find_distance(graph, 3, 1) == -1


def test_distance_takes_the_shortest(distance_mod):
    graph = {1: [2, 4], 2: [3], 3: [4], 4: []}
    assert distance_mod.find_distance(graph, 1, 4) == 1


# Most reliable path

def test_reliable_path(reliable_mod):
    edges = [(0, 1, 50), (1, 2, 50), (0, 2, 20)]
    reliability, path = reliable_mod.most_reliable_path(3, edges, 0, 2)
    assert reliability == pytest.approx(25.0)
    assert path == [0, 1, 2]


def test_reliable_path_direct_edge_wins(reliable_mod):
    edges = [(0, 1, 50), (1, 2, 50), (0, 2, 80)]
    reliability, path = reliable_mod.most_reliable_path(3, edges, 0, 2)
    assert reliability == pytest.approx(80.0)
    assert path == [0, 2]


def test_reliable_path_no_path(reliable_mod):
    assert reliable_mod.most_reliable_path(3, [(0, 1, 50)], 0, 2) is None


def test_reliable_path_same_node(reliable_mod):
    reliability, path = reliable_mod.most_reliable_path(2, [(0, 1, 50)], 0, 0)
    assert reliability == pytest.approx(100.0)
    assert path == [0]


# Cheap town tour (Kruskal)

def test_cheapest_tour(tour_mod):
    edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4)]
    total_cost, used_edges = tour_mod.cheapest_tour(4, edges)
    assert total_cost == 7
    assert used_edges == [(0, 1, 1), (1, 2, 2), (2, 3, 4)]


def test_cheapest_tour_no_edges(tour_mod):
    assert tour_mod.cheapest_tour(1, []) == (0, [])


def test_cheapest_tour_two_separate_parts(tour_mod):
    edges = [(0, 1, 5), (2, 3, 6)]
    assert tour_mod.cheapest_tour(4, edges) == (11, [(0, 1, 5), (2, 3, 6)])


# Undefined (Bellman-Ford)

def test_bellman_ford_path(undefined_mod):
    edges = [(1, 2, 4), (2, 3, -2), (1, 3, 5)]
    assert undefined_mod.shortest_path_bellman_ford(3, edges, 1, 3) == ([1, 2, 3], 2)


def test_bellman_ford_undefined(undefined_mod):
    edges = [(1, 2, 1), (2, 3, -3), (3, 2, 1)]
    assert undefined_mod.shortest_path_bellman_ford(3, edges, 1, 3) is None


def test_bellman_ford_unreachable(undefined_mod):
    path, distance = undefined_mod.shortest_path_bellman_ford(3, [(1, 2, 1)], 1, 3)
    assert path == [3]
    assert distance == INF


def test_bellman_ford_source_is_destination(undefined_mod):
    assert undefined_mod.shortest_path_bellman_ford(2, [(1, 2, 3)], 1, 1) == ([1], 0)


# Cable network (Prim with a budget)

def network_edges():
    # (first, second, weight, already_in_tree)
    return [
        (0, 1, 10, True),
        (1, 2, 5, False),
        (2, 3, 3, False),
        (0, 3, 20, False),
    ]


def test_network_big_budget(network_mod):
    assert network_mod.budget_used_by_network(100, 4, network_edges()) == 8


def test_network_budget_for_one_edge(network_mod):
    assert network_mod.budget_used_by_network(6, 4, network_edges()) == 5


def test_network_budget_too_small(network_mod):
    assert network_mod.budget_used_by_network(4, 4, network_edges()) == 0


def test_network_no_tree_edges(network_mod):
    edges = [(0, 1, 5, False), (1, 2, 5, False)]
    assert network_mod.budget_used_by_network(100, 3, edges) == 0
