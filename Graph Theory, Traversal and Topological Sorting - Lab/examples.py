# Adjacency list # the specific index is the parent
from collections import deque

print("Types of graphs")
print("----------------------------------------------")

list_graph = [
    [],
    [2, 4],
    [3],
    [1],
    [2]
]

print(f"Adjacency list: {list_graph[1]}")  # presents the children of the specific parent.
# --------------------------------------------------------------------

# Adjacency matrix # the specific index is the parent
matrix_graph = [
    [],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
    [1, 0, 0, 0],
    [0, 1, 0, 0]
]

print(f"Adjacency matrix: {matrix_graph[1]}")  # presents all links for the specific parent (0 - False, 1 - True)
# --------------------------------------------------------------------

# List of edges # the specific index is the parent
edges_graph = [
    {1, 2},
    {1, 4},
    {2, 3},
    {3, 1},
    {4, 2}
]

print(f"List of edges: {edges_graph[1]}")  # presents the edges (parent, child) of the specific parent
# --------------------------------------------------------------------

# Dictionary # the specific key is the parent
dictionary_graph = {
    1: [2, 4],
    2: [3],
    3: [1],
    4: [2]
}

print(f"Dictionary graph: {dictionary_graph[1]}")  # presents the children of the specific parent.


# --------------------------------------------------------------------

# DFS Algorithm
def dfs(node, graph, visited):
    if node in visited:
        return

    visited.add(node)

    for child in graph[node]:
        dfs(child, graph, visited)

    print(node, end=" ")


dict_graph = {
    7: [19, 21, 14],
    19: [1, 12, 31, 21],
    1: [7],
    12: [],
    31: [21],
    21: [14],
    14: [23, 6],
    6: [],
    23: [21]
}

visited = set()

print('DFS Algorithm:', end=" ")

for node in dict_graph:
    dfs(node, dict_graph, visited)

# ----------------------------------------------
print()


def second_dfs(node, graph, visited):
    if visited[node]:
        return

    visited[node] = True

    for child in graph[node]:
        second_dfs(child, graph, visited)

    print(node, end=" ")


second_list_graph = [
    [3, 6],
    [2, 3, 4, 5, 6],
    [1, 4, 5],
    [0, 1, 5],
    [1, 2, 6],
    [1, 2, 3],
    [0, 1, 4]
]

len_graph = len(second_list_graph)
second_visited = [False] * len_graph

print("DFS Algorithm:", end=" ")

for node in range(len_graph):
    second_dfs(node, second_list_graph, second_visited)

# --------------------------------------------------------------------
# BFS Algorithm
print()


def bfs(node, graph, visited):
    if node in visited:
        return

    queue = deque([node])
    visited.add(node)

    while queue:
        current_node = queue.popleft()
        print(current_node, end=" ")

        for child in graph[current_node]:
            if child not in visited:
                visited.add(child)
                queue.append(child)


bfs_visited = set()

print("BFS Algorithm:", end=" ")

for node in dict_graph:
    bfs(node, dict_graph, bfs_visited)
