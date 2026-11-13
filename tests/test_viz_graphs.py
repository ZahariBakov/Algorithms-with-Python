import random
from collections import deque

from viz.algorithms.graphs import (
    SAMPLE_GRAPH,
    SAMPLE_POSITIONS,
    bfs,
    bfs_order,
)
from viz.steps import DONE, FOUND, VISIT


def plain_bfs(graph, start):
    order = []
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return order


def random_graph(size, rng):
    graph = {i: [] for i in range(size)}
    for i in range(size):
        for j in range(i + 1, size):
            if rng.random() < 0.3:
                graph[i].append(j)
                graph[j].append(i)
    return graph


def test_sample_graph_is_valid():
    assert len(SAMPLE_GRAPH) == 8
    assert set(SAMPLE_POSITIONS) == set(SAMPLE_GRAPH)
    for node, neighbors in SAMPLE_GRAPH.items():
        for other in neighbors:
            assert node in SAMPLE_GRAPH[other]


def test_order_matches_plain_bfs_from_every_start():
    for start in SAMPLE_GRAPH:
        assert bfs_order(bfs(SAMPLE_GRAPH, start)) == plain_bfs(SAMPLE_GRAPH, start)


def test_order_matches_plain_bfs_on_random_graphs():
    rng = random.Random(1)
    for _ in range(30):
        graph = random_graph(rng.randint(1, 12), rng)
        start = rng.choice(list(graph))
        assert bfs_order(bfs(graph, start)) == plain_bfs(graph, start)


def test_every_node_is_visited_once():
    order = bfs_order(bfs(SAMPLE_GRAPH, 0))
    assert sorted(order) == sorted(SAMPLE_GRAPH)
    visits = [s.indices[0] for s in bfs(SAMPLE_GRAPH, 0) if s.kind == VISIT]
    assert sorted(visits) == sorted(SAMPLE_GRAPH)


def test_one_node_graph():
    steps = list(bfs({0: []}, 0))
    assert [s.kind for s in steps] == [VISIT, DONE]
    assert steps[-1].info == [0]


def test_unreachable_nodes_are_not_visited():
    graph = {0: [1], 1: [0], 2: []}
    assert bfs_order(bfs(graph, 0)) == [0, 1]


def test_generator_ends():
    steps = bfs(SAMPLE_GRAPH, 0)
    items = list(steps)
    assert items[-1].kind == DONE
    assert next(steps, None) is None


def test_steps_copy_visited_and_queue():
    steps = list(bfs(SAMPLE_GRAPH, 0))
    # Every step has its own lists.
    for a, b in zip(steps, steps[1:]):
        assert a.data is not b.data
        assert a.info is not b.info
    # Old steps do not change when the search goes on.
    assert steps[0].data == [0]
    assert steps[0].info == []
    found = [s for s in steps if s.kind == FOUND]
    assert found[0].info == [1]
    assert steps[-1].data is not steps[-1].info
