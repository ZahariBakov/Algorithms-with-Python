def dfs(node, graph, visited, cycles):
    if node in cycles:
        raise Exception

    if node in visited:
        return

    visited.add(node)
    cycles.add(node)

    for child in graph[node]:
        dfs(child, graph, visited, cycles)

    cycles.remove(node)


def is_acyclic(graph):
    visited = set()

    try:
        for node in graph:
            dfs(node, graph, visited, set())
        return True
    except Exception:
        return False


def main():
    command = input()
    graph = {}

    while command != "End":
        parent, child = command.split("-")

        if parent not in graph:
            graph[parent] = []

        if child not in graph:
            graph[child] = []

        graph[parent].append(child)

        command = input()

    if is_acyclic(graph):
        print("Acyclic: Yes")
    else:
        print("Acyclic: No")


if __name__ == '__main__':
    main()
