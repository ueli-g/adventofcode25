from heapq import heappush, heappop
import numpy as np

def solve_a(filename):
    with open(filename) as infile:
        lines = [l.strip() for l in infile.readlines()]
        points = np.zeros(shape=(len(lines),2), dtype=np.int64)
        for i, line in enumerate(lines):
            points[i] = [int(c) for c in line.split(',')]
    mp = np.mean(points, 0)
    points = points - mp
    norms = np.linalg.norm(points,ord=1,axis=1)

    class HeapEntry:
        def __init__(self, norm, point):
            self.norm = norm
            self.point = point
        def __lt__(self, other):
            return self.norm < other.norm
        def __repr__(self):
            return f"HeapEntry({self.norm}: {self.point})"


    mheap = []
    for n,p in zip(norms,points):
        heappush(mheap, HeapEntry(n,p))

    mlist = [HeapEntry(n,p) for n,p in zip(norms, points)]

    mlist.sort()
    mlist = mlist[::-1]

    largest_area = 0
    for i, pi in enumerate(mlist[:-1]):
        for pj in mlist[i+1:]:
            l1sum = pi.norm + pj.norm + 2
            sup_area = (l1sum / 2)**2
            if sup_area < largest_area:
                break
            edges = np.abs(pi.point - pj.point) + np.ones(shape=(2))
            this_area = np.prod(edges)
            if this_area > largest_area:
                largest_area = this_area
            print()
    return largest_area

def solve_b(filename):
    with open(filename) as infile:
        lines = [l.strip() for l in infile.readlines()]
        points = np.zeros(shape=(len(lines),2), dtype=np.int64)
        for i, line in enumerate(lines):
            points[i] = [int(c) for c in line.split(',')]
    mp = np.mean(points, 0)
    meanpoints = points - mp
    norms = np.linalg.norm(meanpoints,ord=1,axis=1)

    class HeapEntry:
        def __init__(self, norm, point):
            self.norm = norm
            self.point = point
        def __lt__(self, other):
            return self.norm < other.norm
        def __repr__(self):
            return f"HeapEntry({self.norm}: {self.point})"


    edges = np.zeros(shape=points.shape,dtype=np.int64)
    for m,v in enumerate(points[1:,:]):
        edges[m] = v - points[m,:]
    edges[-1] = points[0] - points[-1]
    corner_angles = np.zeros(shape=(edges.shape[0],1),dtype=np.int64)
    index = 0
    for e1,e2 in zip(edges[:-1], edges[1:]):
        corner_angles[index] = np.cross(e1,e2)/(np.linalg.norm(e1)*np.linalg.norm(e2))
        index += 1

    # corner_angles should sum to +3 for positive loop, to -3 for negative loop
    is_positive = sum(corner_angles) >= 0
    inside_directions = np.zeros(edges.shape,dtype=np.int64)

    for i,e in enumerate(edges):
        z = np.array((0,0,1 if is_positive else -1))
        e3 = np.array((e[0], e[1], 0))
        inside_directions[i] = np.cross(z,e)[:2]/np.linalg.norm(e3)

    inside_map = dict()
    for i,v in enumerate(points):
        inside_map[(v[0], v[1])] = inside_directions[i-1] + inside_directions[i]

    mheap = []
    for n,p in zip(norms,points):
        heappush(mheap, HeapEntry(n,p))

    mlist = [HeapEntry(n,p) for n,p in zip(norms, points)]

    _ord = mlist.sort()
    mlist = mlist[::-1]


    def check_intersection(ci,cj,xmin,xmax,ymin,ymax):
        dc = cj-ci
        if dc[0] == 0:
            #vertical
            if ci[0] > xmin and cj[0] < xmax:
                # going through box vertically
                if min(ci[1],cj[1]) >= ymax:
                    #both above
                    pass
                elif max(ci[1],cj[1]) <= ymin:
                    #both below
                    pass
                else:
                    return True
        elif dc[1] == 0:
            #horizontal
            if ci[1] > ymin and cj[1] < ymax:
                # going through horizontal
                if min(ci[0],cj[0]) >= xmax:
                    #both right
                    pass
                elif max(ci[0],cj[0]) <= xmin:
                    #both left
                    pass
                else:
                    return True
        return False


    largest_area = 0
    for i, pi in enumerate(mlist[:-1]):
        for pj in mlist[i+1:]:
            xmin = min(pi.point[0],pj.point[0])
            xmax = max(pi.point[0],pj.point[0])
            ymin = min(pi.point[1],pj.point[1])
            ymax = max(pi.point[1],pj.point[1])

            this_area = (xmax - xmin + 1)*(ymax - ymin + 1)
            if this_area < largest_area:
                continue


            inside = False
            for cursor in mlist:
                x,y = cursor.point
                on = x >= xmin and x <= xmax and y >= ymin and y <= ymax
                inside = x > xmin and x < xmax and y > ymin and y < ymax
                if inside:
                    break

            if inside:
                continue

            collision = False
            for ci, cj in zip(points[:-1],points[1:]):
                collision = collision or check_intersection(ci,cj,xmin,xmax,ymin,ymax)
                if collision:
                    break
            collision = collision or check_intersection(points[-1],points[0],xmin,xmax,ymin,ymax)
            if collision:
                continue
      
            if this_area > largest_area:
                largest_area = this_area
                print(largest_area)
    return largest_area

sta = solve_a('test.txt')
sia = solve_a('input.txt')

stb = solve_b('test.txt')
stb = solve_b('input.txt')
