def find_root(parent, node):
    while node != parent[node]:
        node = parent[node]

    return node


nodes = int(input())
edges = int(input())

graph = []
parent = [num for num in range(nodes)]
total_cost = 0

for _ in range(edges):
    source, destination, weight = [int(x) for x in input().split(" - ")]
    graph.append((source, destination, weight))

for first, second, weight in sorted(graph, key=lambda x: x[2]):
    first_node_root = find_root(parent, first)
    second_node_root = find_root(parent, second)

    if first_node_root == second_node_root:
        continue

    parent[first_node_root] = second_node_root
    total_cost += weight

    # if want to see the edges:
    print(f"{{{first} - {second}}} - {weight}")

print(f"Total cost: {total_cost}")
