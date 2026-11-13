def dfs(node, destination, graph, visited):
    if node in visited:
        return

    visited.add(node)

    if node == destination:
        return

    for child in graph[node]:
        dfs(child, destination, graph, visited)


def path_exists(source, destination, graph):
    visited = set()

    dfs(source, destination, graph, visited)

    return destination in visited


def find_edges_to_remove(graph):
    edges = []
    remove_edges = []

    for node, children in graph.items():
        for child in children:
            edges.append((node, child))

    for source, destination in sorted(edges, key=lambda x: (x[0], x[1])):
        if destination not in graph[source] or source not in graph[destination]:
            continue

        graph[source].remove(destination)
        graph[destination].remove(source)

        if path_exists(source, destination, graph):
            remove_edges.append((source, destination))
        else:
            graph[source].append(destination)
            graph[destination].append(source)

    return remove_edges


def main():
    nodes = int(input())
    graph = {}

    for _ in range(nodes):
        node, children_str = input().split(" -> ")
        children = children_str.split()
        graph[node] = children

    remove_edges = find_edges_to_remove(graph)

    print(f"Edges to remove: {len(remove_edges)}")

    for first, second in remove_edges:
        print(f"{first} - {second}")


if __name__ == '__main__':
    main()
