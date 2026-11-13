def dfs(node, graph, visited, component):
    if visited[node]:
        return

    visited[node] = True

    for child in graph[node]:
        dfs(child, graph, visited, component)

    component.append(node)


def find_components(graph):
    nodes = len(graph)
    visited = [False] * nodes
    components = []

    for node in range(nodes):
        component = []
        if visited[node]:
            continue
        dfs(node, graph, visited, component)

        components.append(component)

    return components


def main():
    nodes = int(input())
    graph = []

    for _ in range(nodes):
        graph.append([int(x) for x in input().split()])

    for component in find_components(graph):
        print(f"Connected component: {' '.join([str(x) for x in component])}")


if __name__ == '__main__':
    main()
