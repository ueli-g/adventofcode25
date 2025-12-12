import numpy as np

with open('test.txt') as infile:
    lines = [l.strip() for l in infile.readlines()]

M = len(lines)

vertices = np.zeros(shape=(M,2),dtype=np.int64)
edges = np.zeros(shape=(M,2),dtype=np.int64)

for m,line in enumerate(lines):
    vertices[m,:] = [int(c) for c in line.split(',')]

for m,v in enumerate(vertices[1:,:]):
    edges[m] = v - vertices[m,:]

edges[-1] = vertices[0] - vertices[-1]

corner_angles = np.zeros(shape=(M,1),dtype=np.int64)

index = 0
for e1,e2 in zip(edges[:-1], edges[1:]):
    corner_angles[index] = np.cross(e1,e2)/(np.linalg.norm(e1)*np.linalg.norm(e2))
    index += 1

# corner_angles should sum to +3 for positive loop, to -3 for negative loop
is_positive = sum(corner_angles) >= 0

inside_directions = np.zeros((M,2),dtype=np.int64)

for i,e in enumerate(edges):
    z = np.array((0,0,1 if is_positive else -1))
    e3 = np.array((e[0], e[1], 0))
    inside_directions[i] = np.cross(z,e)[:2]/np.linalg.norm(e3)

inside_map = dict()
for i,v in enumerate(vertices):
    inside_map[(v[0], v[1])] = inside_directions[i-1] + inside_directions[i]

GLOBAL_VERTEX_SET = set()
for v in vertices:
    GLOBAL_VERTEX_SET.add((v[0],v[1]))

xmin, ymin = np.min(vertices, 0)
xmax, ymax = np.max(vertices, 0)

class Node:
    def __init__(self, corners, edge_map, inside_map, _memo):
        xmin = min(corners[0][0], corners[1][0])
        xmin = max(corners[0][0], corners[1][0])
        ymin = min(corners[0][1], corners[1][1])
        xmin = max(corners[0][1], corners[1][1])

        self.min = (xmin, ymin)
        self.max = (xmax, ymax)
        self.inside_map = dict()
        self.edge_map = dict()
        for v,val in edge_map.items():
            if self.inside_inclusive(v):
                if self.inside_exclusive(v):
                    self.inside_map[v] = val
                else:
                    self.edge_map[v] = val
        for v,val in inside_map.items():
            if self.inside_inclusive(v):
                if self.inside_exclusive(v):
                    self.inside_map[v] = val
                else:
                    self.edge_map[v] = val
        self.memo = _memo
        self.children = []
        self.search()
    def search(self):
        for su in self.get_subareas():
            self.children.append(Node(su,self.edge_map, self.inside_map,self.memo))
        if len(self.children) == 0 and len(self.inside_map) == 0:
            print(self)
    def __repr__(self):
        area = (self.max[0] - self.min[0] + 1) * (self.max[1] - self.min[1] + 1)
        return f"Node({self.min},{self.max}) area {area}"
    def inside_exclusive(self, v):
        if v[0] > self.min[0] and v[1] > self.min[1]:
            if v[0] < self.max[0] and v[1] < self.max[1]:
                return True
        return False
    def inside_inclusive(self, v):
        if v[0] >= self.min[0] and v[1] >= self.min[1]:
            if v[0] <= self.max[0] and v[1] <= self.max[1]:
                return True
        return False
        
    def get_subareas(self):
        pos_candidates = []
        for k,v in self.inside_map.items():
            x,y = k
            xdir, ydir = v

            pos_candidates.append([
                ((x,self.min[1]),self.max),
                (self.min,(x,self.max[1])),
                ((self.min[0],y), self.max),
                ((self.min),(self.max[0],y))
            ])

        for k,v in self.edge_map.items():
            x,y = k
            xdir, ydir = v
            
            indir = inside_directions[()]

            pos_candidates.append([
                ((x,self.min[1]),self.max),
                (self.min,(x,self.max[1])),
                ((self.min[0],y), self.max),
                ((self.min),(self.max[0],y))
            ])

        for min, max in pos_candidates:
            if (min,max) == (self.min,self.max):
                continue

            opposite_0 = (min[0],max[1])
            opposite_1 = (max[0],min[1])        
            if (min in GLOBAL_VERTEX_SET and max in GLOBAL_VERTEX_SET) or \
                    (opposite_0 in GLOBAL_VERTEX_SET and opposite_1 in GLOBAL_VERTEX_SET):
                yield (min,max)

        
memo = dict()
corners = ((xmin, ymin), (xmax,ymax))

node = Node(corners, inside_map, inside_map, memo)
        

print()