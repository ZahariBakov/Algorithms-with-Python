from collections import deque
from queue import PriorityQueue
class Edge:
    def __init__(self, first, second, weight):
        self.first = first
        self.second = second
        self.weight = weight


nodes = int(input())
edges = int(input())

graph = []
[graph.append([]) for _ in range(nodes)]

for _ in range(edges):
    first, second, weight = [int(x) for x in input().split()]
    edge = Edge(first, second, weight)
    graph[first].append(edge)
    graph[second].append(edge)

source = int(input())
destination = int(input())

pq = PriorityQueue()
pq.put((-100, source))

distance = [float("-inf")] * nodes
distance[source] = 100

parent = [None] * nodes


while not pq.empty():
    max_distance, node = pq.get()

    if node == destination:
        break

    for edge in graph[node]:
        child = edge.second if edge.first == node else edge.first
        new_distance = -max_distance * edge.weight / 100

        if new_distance > distance[child]:
            distance[child] = new_distance
            parent[child] = node
            pq.put((-new_distance, child))

print(f"Most reliable path reliability: {distance[destination]:.2f}%")

queue = deque()
node = destination

while node is not None:
    queue.appendleft(node)
    node = parent[node]

print(*queue, sep=" -> ")
