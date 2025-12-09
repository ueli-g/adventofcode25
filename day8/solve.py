import math
from heapq import heappush, heappop

class Graph:
    def __init__(self, V):
        self.v = set(V)
    def __repr__(self):
        return f"Graph({self.v})"
    def __len__(self):
        return len(self.v)
    def __hash__(self):
        return hash(frozenset(self.v))
    def __contains__(self,other):
        return other in self.v
    def distance(m,n):
        return math.sqrt(sum((m-n)**2 for m,n in zip(m,n)))
    #def min_distance_from(self, node):
    #    return Graph.distance(node, self.v[0]) - len(self)
    def closest_node_from(self, pos):
        closest_distance = float('inf')
        closest_node = None
        for v in self.v:
            if Graph.distance(pos,v) < closest_distance:
                closest_node = v
        return closest_node
    def merge(self, other):
        self.v = self.v.union(other.v)
        return self

class HeapEntry:
    def __init__(self, a, b, circuit):
        self.a = a
        self.b = b
        self.circuit = circuit
        self.cost = Graph.distance(self.a, self.b)
    def __lt__(self, other):
        return self.cost < other.cost
    def __repr__(self):
        return f"Edge {self.a} to {self.b}:{self.cost}"

filename = 'test.txt'

nodes = list()
circuits = list()
circuit_map = dict()

with open(filename) as infile:
    lines = infile.readlines()
    for line in lines:
        pos = tuple(int(coord) for coord in line.strip().split(','))
        graph = Graph((pos,))
        circuits.append(graph)
        circuit_map[pos] = graph
        nodes.append(pos)

processed = set()

shortest = dict()
for i, n in enumerate(nodes[:-1]):
    candidate_cost = float('inf')
    processed.add(n)
    neighbour = None
    #closest_circuit = None
    for j,o in enumerate(nodes[i+1:]):
        this_cost = Graph.distance(n,o)
        pos_set = frozenset((n,o))
        old_cost = shortest.get(pos_set, float('inf'))
        if this_cost < old_cost:
            shortest[pos_set] = this_cost


heaplist = list()
for k, v in shortest.items():
    k0, k1 = list(k)
    entry = HeapEntry(k0, k1, v)
    heappush(heaplist, entry)
    #for j, c in enumerate(circuits):
    #    if c.min_distance_from(n) < candidate_cost:
    #        #closest_node = c.closest_node_from(n)
    #        #if n == closest_node:
    #        #    continue
    #        this_cost = Graph.distance(n,closest_node)
    #        if this_cost < candidate_cost:
    #            neighbour = closest_node
    #            closest_circuit = c
    #            candidate_cost = this_cost
    #fs = frozenset((n,neighbour))
    #if fs not in processed:
    #    entry = HeapEntry(n, neighbour, closest_circuit)
    #    heappush(heaplist, entry)
    #processed.add(fs)
print(i)


count = 0
while count <= 10 and len(heaplist) > 0:
    entry = heappop(heaplist)
    a = entry.a
    b = entry.b
    g1 = circuit_map[a]
    g2 = circuit_map[b]
    if g1 != g2:
        g1.merge(g2)
        circuit_map[b] = g1
        count += 1


    print(len(heaplist))    
    print(entry)


vset = set(circuit_map.values())

lengths = [len(s) for s in vset]
lengths.sort()

print()