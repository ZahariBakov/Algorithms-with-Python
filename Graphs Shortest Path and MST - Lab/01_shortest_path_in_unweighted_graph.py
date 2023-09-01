def find_parent_by_node(graph, start, destination):
    visited = [False] * len(graph)
    parent = [None] * len(graph)

    visited[start] = True

    queue = deque([start])

    while queue:
        node = queue.popleft()

        if node == destination:
            break

        for child in graph[node]:
            if visited[child]:
                continue

            visited[child] = True
            queue.append(child)
            parent[child] = node

    return parent


def reconstruct_path(parent, destination):
    path = deque()
    node = destination

    while node is not None:
        path.appendleft(node)
        node = parent[node]

    return path


from collections import deque

nodes = int(input())
edges = int(input())

graph = []
[graph.append([]) for _ in range(nodes + 1)]

for _ in range(edges):
    start, destination = [int(x) for x in input().split()]
    graph[start].append(destination)

start_node = int(input())
destination_node = int(input())

parent = find_parent_by_node(graph, start_node, destination_node)

path = reconstruct_path(parent, destination_node)

print(f"Shortest path length is: {len(path) - 1}")
print(*path)
