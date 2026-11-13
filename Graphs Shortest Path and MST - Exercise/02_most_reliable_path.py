from collections import deque
from queue import PriorityQueue
class Edge:
    def __init__(self, first, second, weight):
        self.first = first
        self.second = second
        self.weight = weight


def most_reliable_path(nodes, edges, source, destination):
    graph = []
    [graph.append([]) for _ in range(nodes)]

    for first, second, weight in edges:
        edge = Edge(first, second, weight)
        graph[first].append(edge)
        graph[second].append(edge)

    pq = PriorityQueue()
    pq.put((-100, source))

    distance = [float("-inf")] * nodes
    distance[source] = 100

    parent = [None] * nodes

    while not pq.empty():
        max_distance, node = pq.get()

        if node == destination:
            break

        for edge in graph[node]:
            child = edge.second if edge.first == node else edge.first
            new_distance = -max_distance * edge.weight / 100

            if new_distance > distance[child]:
                distance[child] = new_distance
                parent[child] = node
                pq.put((-new_distance, child))

    if distance[destination] == float("-inf"):
        return None

    queue = deque()
    node = destination

    while node is not None:
        queue.appendleft(node)
        node = parent[node]

    return distance[destination], list(queue)


def main():
    nodes = int(input())
    edges_count = int(input())

    edges = []

    for _ in range(edges_count):
        first, second, weight = [int(x) for x in input().split()]
        edges.append((first, second, weight))

    source = int(input())
    destination = int(input())

    result = most_reliable_path(nodes, edges, source, destination)

    if result is None:
        print("There is no path between the two nodes")
    else:
        reliability, path = result
        print(f"Most reliable path reliability: {reliability:.2f}%")

        print(*path, sep=" -> ")


if __name__ == '__main__':
    main()
