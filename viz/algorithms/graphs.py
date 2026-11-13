from collections import deque

from viz.steps import DONE, FOUND, VISIT, Step

# A small graph with 8 nodes. Each node has a list of neighbors.
SAMPLE_GRAPH = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 4, 5],
    3: [1, 6],
    4: [1, 2, 6],
    5: [2, 7],
    6: [3, 4, 7],
    7: [5, 6],
}

# Node positions on the screen, from 0 to 1 (x, y).
SAMPLE_POSITIONS = {
    0: (0.10, 0.50),
    1: (0.28, 0.20),
    2: (0.28, 0.80),
    3: (0.50, 0.10),
    4: (0.50, 0.50),
    5: (0.50, 0.90),
    6: (0.72, 0.30),
    7: (0.90, 0.60),
}


def bfs(graph, start):
    """Breadth first search from start. Yields Step objects.

    A node is marked as seen when it goes into the queue, so it
    goes in only once.
    """
    visited = []
    queue = deque([start])
    seen = {start}
    while queue:
        node = queue.popleft()
        visited.append(node)
        yield Step(VISIT, (node,), visited[:], list(queue))
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
                yield Step(FOUND, (neighbor,), visited[:], list(queue))
    yield Step(DONE, (), visited[:], visited[:])


def dfs(graph, start):
    """Depth first search from start. Yields Step objects.

    It uses a stack. A node is marked as visited when it comes off the
    stack, so the order is the same as in a recursive DFS. The same node
    can be on the stack more than once. A node that is already visited
    is skipped. Neighbors are used in sorted order.
    """
    visited = []
    done = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in done:
            continue
        done.add(node)
        visited.append(node)
        yield Step(VISIT, (node,), visited[:], stack[:])
        # Push in reverse, so the smallest neighbor is on top.
        for neighbor in sorted(graph[node], reverse=True):
            if neighbor not in done:
                stack.append(neighbor)
                yield Step(FOUND, (neighbor,), visited[:], stack[:])
    yield Step(DONE, (), visited[:], visited[:])


def _last_info(steps):
    last = None
    for last in steps:
        pass
    return last.info


def bfs_order(steps):
    """The BFS order, read from the last step."""
    return _last_info(steps)


def dfs_order(steps):
    """The DFS order, read from the last step."""
    return _last_info(steps)
