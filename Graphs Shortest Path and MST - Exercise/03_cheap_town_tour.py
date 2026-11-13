def find_root(parent, node):
    while node != parent[node]:
        node = parent[node]

    return node


def cheapest_tour(nodes, edges):
    graph = []
    parent = [num for num in range(nodes)]
    total_cost = 0
    used_edges = []

    for source, destination, weight in edges:
        graph.append((source, destination, weight))

    for first, second, weight in sorted(graph, key=lambda x: x[2]):
        first_node_root = find_root(parent, first)
        second_node_root = find_root(parent, second)

        if first_node_root == second_node_root:
            continue

        parent[first_node_root] = second_node_root
        total_cost += weight
        used_edges.append((first, second, weight))

    return total_cost, used_edges


def main():
    nodes = int(input())
    edges_count = int(input())

    edges = []

    for _ in range(edges_count):
        source, destination, weight = [int(x) for x in input().split(" - ")]
        edges.append((source, destination, weight))

    total_cost, used_edges = cheapest_tour(nodes, edges)

    for first, second, weight in used_edges:
        # if want to see the edges:
        print(f"{{{first} - {second}}} - {weight}")

    print(f"Total cost: {total_cost}")


if __name__ == '__main__':
    main()
