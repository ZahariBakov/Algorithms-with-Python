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


def shortest_path(nodes, edges, start_node, destination_node):
    graph = []
    [graph.append([]) for _ in range(nodes + 1)]

    for start, destination in edges:
        graph[start].append(destination)

    parent = find_parent_by_node(graph, start_node, destination_node)

    path = reconstruct_path(parent, destination_node)

    if path[0] != start_node:
        return None

    return list(path)


def main():
    nodes = int(input())
    edges_count = int(input())

    edges = []

    for _ in range(edges_count):
        start, destination = [int(x) for x in input().split()]
        edges.append((start, destination))

    start_node = int(input())
    destination_node = int(input())

    path = shortest_path(nodes, edges, start_node, destination_node)

    if path is None:
        print("There is no path between the two nodes")
    else:
        print(f"Shortest path length is: {len(path) - 1}")
        print(*path)


if __name__ == '__main__':
    main()
