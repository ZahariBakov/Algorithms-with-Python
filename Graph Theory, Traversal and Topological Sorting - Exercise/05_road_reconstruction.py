def dfs(node, graph, visited):
    if visited[node]:
        return

    visited[node] = True

    for child in graph[node]:
        dfs(child, graph, visited)


def find_important_streets(nodes, streets):
    graph = []
    [graph.append([]) for _ in range(nodes)]

    # edges = set()
    edges = []
    result = []

    for first, second in streets:
        graph[first].append(second)
        graph[second].append(first)
        # edges.add((min(first, second), max(first, second)))
        edges.append((min(first, second), max(first, second)))

    for first, second in edges:
        graph[first].remove(second)
        graph[second].remove(first)

        visited = [False] * nodes

        dfs(0, graph, visited)

        if not all(visited):
            result.append((first, second))

        graph[first].append(second)
        graph[second].append(first)

    return result


def main():
    nodes = int(input())
    edges_count = int(input())
    streets = []

    for _ in range(edges_count):
        first, second = [int(x) for x in input().split(" - ")]
        streets.append((first, second))

    print("Important streets:")

    for first, second in find_important_streets(nodes, streets):
        print(first, second)


if __name__ == '__main__':
    main()
