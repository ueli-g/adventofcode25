import math
from scipy import spatial
import numpy as np
from heapq import heappush, heappop

class Graph:
    def __init__(self, V):
        self.v = set(V)
    def __len__(self):
        return len(self.v)
    def __hash__(self):
        return hash(frozenset(self.v))
    def __gt__(self, other):
        return len(self) > len(other)
    def merge(self, other):
        self.v = self.v.union(other.v)
        return self

def parse_points(filename):
    with open(filename) as infile:
        lines = infile.readlines()
        points = np.empty(shape=(len(lines),3), dtype=np.int64)
        for nline, line in enumerate(lines):
            pos = tuple(int(coord) for coord in line.strip().split(','))
            points[nline] = pos
            #circuit_map[pos] = graph
    return points

def distance(a,b):
    return np.linalg.norm(a-b)

def edge_list_delaunay(points):
    shortest = dict()
    checked = set()
    mlist = []

    delaunay = spatial.Delaunay(points, incremental=False)
    assert(len(delaunay.coplanar) == 0)

    for ki, k1 in enumerate(delaunay.vertex_neighbor_vertices[0][:-1]):
        k2 = delaunay.vertex_neighbor_vertices[0][ki+1]
        for candidate in delaunay.vertex_neighbor_vertices[1][k1:k2]:
            marker = frozenset((ki, int(candidate)))
            if marker not in checked:
                dist = distance(points[ki], points[candidate])
                shortest[marker] = distance(points[ki], points[candidate])
                heappush(mlist, (dist,marker))
                checked.add(marker)
    return mlist

def edge_list_brute(points):
    shortest = dict()
    checked = set()
    mlist = []

    for i, pi in enumerate(points[:-1]):
        for j, pj in enumerate(points[i+1:]):
            marker = (i, i+j+1)
            if marker not in checked:
                dist = distance(pi, pj)
                heappush(mlist, (dist,marker))
                checked.add(marker)
        print(i)
    return mlist

def solve_a(filename, edge_count):
    points = parse_points(filename)
    mlist = edge_list_brute(points)
    circuits = [Graph((pi,)) for pi in range(len(points))]
    circuitmap = {pi:Graph((pi,)) for pi in range(len(points))}

    count = 0
    while len(mlist) > 0 and count < edge_count:
        cost, nodes = heappop(mlist)
        m, n = list(nodes)
        cm = circuitmap[m]
        cn = circuitmap[n]
        cm.merge(cn)
        for c in cm.v:
            circuitmap[c] = cm
        count += 1

    graphs = list(set(circuitmap.values()))
    graphs.sort()
    asum = len(graphs[-1]) * len(graphs[-2]) * len(graphs[-3])
    return asum

def solve_b(filename):
    points = parse_points(filename)
    mlist = edge_list_brute(points)
    circuits = [Graph((pi,)) for pi in range(len(points))]
    circuitmap = {pi:Graph((pi,)) for pi in range(len(points))}

    count = 0
    largest_circuit = 0
    xprod = 0
    while largest_circuit < len(points):
        cost, nodes = heappop(mlist)
        m, n = list(nodes)
        
        cm = circuitmap[m]
        cn = circuitmap[n]
        oldsize = max(len(cm), len(cn))

        cm.merge(cn)
        for c in cm.v:
            circuitmap[c] = cm

        newsize = len(cm)
        if newsize > largest_circuit:
            print(f"New longest length at {newsize}")
            print(f"Edge with cost {cost} between {points[m]} - {points[n]}")
            largest_circuit = newsize
            xprod = points[m][0] * points[n][0]
        count += 1
    return xprod

sa = solve_a('test.txt', 10)
sb = solve_b('test.txt')

sa = solve_a('input.txt', 1000)
sb = solve_b('input.txt')

print()