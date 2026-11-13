from collections import deque


def find_path(parent, node):
    result = deque()

    while node is not None:
        result.appendleft(node)
        node = parent[node]

    return result


def shortest_path_bellman_ford(nodes, edges, source, destination):
    graph = list(edges)
    distance = [float("inf")] * (nodes + 1)
    parent = [None] * (nodes + 1)

    distance[source] = 0

    for _ in range(nodes - 1):
        for first, second, weight in graph:
            if distance[first] == float("inf"):
                continue

            new_distance = distance[first] + weight

            if new_distance < distance[second]:
                distance[second] = new_distance
                parent[second] = first

    for first, second, weight in graph:
        new_distance = distance[first] + weight

        if new_distance < distance[second]:
            return None

    path = find_path(parent, destination)

    return list(path), distance[destination]


def main():
    nodes = int(input())
    edges_count = int(input())

    edges = []

    for _ in range(edges_count):
        first, second, weight = [int(x) for x in input().split()]
        edges.append((first, second, weight))

    source = int(input())
    destination = int(input())

    result = shortest_path_bellman_ford(nodes, edges, source, destination)

    if result is None:
        print("Undefined")
    else:
        path, distance = result

        print(*path, sep=" ")
        print(distance)


if __name__ == '__main__':
    main()
