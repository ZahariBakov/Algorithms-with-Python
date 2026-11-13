from queue import PriorityQueue


class Edge:
    def __init__(self, first, second, weight):
        self.first = first
        self.second = second
        self.weight = weight

    def __gt__(self, other):
        return self.weight > other.weight


def budget_used_by_network(budget, nodes, edges):
    tree = set()
    budget_used = 0

    graph = []
    [graph.append([]) for _ in range(nodes)]

    for first, second, weight, in_tree in edges:
        graph[first].append(Edge(first, second, weight))
        graph[second].append(Edge(first, second, weight))

        if in_tree:
            tree.add(first)
            tree.add(second)

    pq = PriorityQueue()

    for node in tree:
        for edge in graph[node]:
            pq.put(edge)

    while not pq.empty():
        min_edge = pq.get()
        non_tree_node = None

        if min_edge.first in tree and min_edge.second not in tree:
            non_tree_node = min_edge.second
        elif min_edge.first not in tree and min_edge.second in tree:
            non_tree_node = min_edge.first

        if non_tree_node is None:
            continue

        if budget_used + min_edge.weight > budget:
            break

        budget_used += min_edge.weight
        tree.add(non_tree_node)

        for edge in graph[non_tree_node]:
            pq.put(edge)

    return budget_used


def main():
    budget = int(input())
    nodes = int(input())
    edges_count = int(input())

    edges = []

    for _ in range(edges_count):
        edges_data = input().split()
        first, second, weight = int(edges_data[0]), int(edges_data[1]), int(edges_data[2])
        edges.append((first, second, weight, len(edges_data) == 4))

    print(f"Budget used: {budget_used_by_network(budget, nodes, edges)}")


if __name__ == '__main__':
    main()
