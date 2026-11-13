from collections import deque


class Edge:
    def __init__(self, source, destination, weight):
        self.source = source
        self.destination = destination
        self.weight = weight


def bellman_ford(nodes, edges, start, target):
    graph = []

    for source, destination, weight in edges:
        graph.append(Edge(source, destination, weight))

    distance = [float("inf")] * (nodes + 1)
    distance[start] = 0
    parent = [None] * (nodes + 1)

    for _ in range(nodes - 1):
        updated = False

        for edge in graph:
            if distance[edge.source] == float("inf"):
                continue

            new_distance = distance[edge.source] + edge.weight

            if new_distance < distance[edge.destination]:
                distance[edge.destination] = new_distance
                parent[edge.destination] = edge.source
                updated = True

        if not updated:
            break

    for edge in graph:
        new_distance = distance[edge.source] + edge.weight

        if new_distance < distance[edge.destination]:
            return "negative cycle", None, None

    if distance[target] == float("inf"):
        return "no path", None, None

    path = deque()
    node = target

    while node is not None:
        path.appendleft(node)
        node = parent[node]

    return "ok", list(path), distance[target]


def main():
    nodes = int(input())
    edges_count = int(input())

    edges = []

    for _ in range(edges_count):
        source, destination, weight = [int(x) for x in input().split()]
        edges.append((source, destination, weight))

    start = int(input())
    target = int(input())

    status, path, distance = bellman_ford(nodes, edges, start, target)

    if status == "negative cycle":
        print("Negative Cycle Detected")
    elif status == "no path":
        print("There is no path to the target")
    else:
        print(*path)
        print(distance)


if __name__ == '__main__':
    main()
