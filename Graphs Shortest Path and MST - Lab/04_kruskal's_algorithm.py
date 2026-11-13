class Edge:
    def __init__(self, first, second, weight):
        self.first = first
        self.second = second
        self.weight = weight


def find_root(parent, node):
    while node != parent[node]:
        node = parent[node]

    return node


def kruskal(edges):
    graph = []
    max_node = float("-inf")

    for first, second, weight in edges:
        graph.append(Edge(first, second, weight))
        max_node = max(first, second, max_node)

    parent = [num for num in range(max_node + 1)]
    forest = []

    for edge in sorted(graph, key=lambda e: e.weight):
        first_node_root = find_root(parent, edge.first)
        second_node_root = find_root(parent, edge.second)

        if first_node_root != second_node_root:
            parent[first_node_root] = second_node_root
            forest.append(edge)

    return [(edge.first, edge.second) for edge in forest]


def main():
    edges_count = int(input())
    edges = []

    for _ in range(edges_count):
        first, second, weight = [int(x) for x in input().split(", ")]
        edges.append((first, second, weight))

    for first, second in kruskal(edges):
        print(f"{first} - {second}")


if __name__ == '__main__':
    main()
