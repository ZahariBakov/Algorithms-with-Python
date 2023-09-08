from queue import PriorityQueue


class Edge:
    def __init__(self, first, second, weight):
        self.first = first
        self.second = second
        self.weight = weight

    def __gt__(self, other):
        return self.weight > other.weight


budget = int(input())
nodes = int(input())
edges = int(input())
tree = set()
budget_used = 0

graph = []
[graph.append([]) for _ in range(nodes)]

for _ in range(edges):
    edges_data = input().split()
    first, second, weight = int(edges_data[0]), int(edges_data[1]), int(edges_data[2])
    graph[first].append(Edge(first, second, weight))
    graph[second].append(Edge(first, second, weight))

    if len(edges_data) == 4:
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

print(f"Budget used: {budget_used}")
