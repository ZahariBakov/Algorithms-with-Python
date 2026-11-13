from collections import deque
from queue import PriorityQueue


class Edge:
    def __init__(self, source, destination, weight):
        self.source = source
        self.destination = destination
        self.weight = weight


def dijkstra(edges, start, target):
    graph = {}

    for source, destination, weight in edges:
        if source not in graph:
            graph[source] = []

        if destination not in graph:
            graph[destination] = []

        graph[source].append(Edge(source, destination, weight))

    max_node = max(graph.keys())

    distance = [float('inf')] * (max_node + 1)
    parent = [None] * (max_node + 1)

    distance[start] = 0

    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        min_distance, node = pq.get()

        if node == target:
            break

        for edge in graph[node]:
            new_distance = min_distance + edge.weight

            if new_distance < distance[edge.destination]:
                distance[edge.destination] = new_distance
                parent[edge.destination] = node
                pq.put((new_distance, edge.destination))

    if distance[target] == float('inf'):
        return None

    path = deque()
    node = target

    while node is not None:
        path.appendleft(node)
        node = parent[node]

    return distance[target], list(path)


def main():
    edges_count = int(input())
    edges = []

    for _ in range(edges_count):
        source, destination, weight = [int(x) for x in input().split(", ")]
        edges.append((source, destination, weight))

    start = int(input())
    target = int(input())

    result = dijkstra(edges, start, target)

    if result is None:
        print("There is no such path.")
    else:
        distance, path = result
        print(distance)

        print(*path)


if __name__ == '__main__':
    main()
