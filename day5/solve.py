
import timeit

class Crange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
    def intersects(self, other):
        return self.start <= other.start <= self.stop
    def __lt__(self, other):
        return self.start < other.start
    def __repr__(self):
        return f"range({self.start},{self.stop})"
    def __add__(self, other):
        self.stop = max(self.stop, other.stop)
        return self
    def __len__(self):
        return self.stop - self.start
    def __contains__(self, num):
        return self.start <= num < self.stop

class RangeTree:
    def __init__(self, ranges):
        self.mid = None
        self.children = ()
        n = len(ranges)
        if n > 1:
            leftranges = ranges[:n//2]
            rightranges = ranges[n//2:]
            self.mid = bisect(leftranges[-1], rightranges[0])
            self.children = (RangeTree(leftranges), RangeTree(rightranges))
        else:
            self.mid = float('inf')
            self.children = (RangeLeaf(ranges[0]),)
    def __contains__(self, num):
        return num in self.children[num > self.mid]

class RangeLeaf:
    def __init__(self, _range):
        self.range = _range
    def __contains__(self, num):
        return num in self.range

def bisect(lrange, rrange):
    assert(rrange.start > lrange.stop)
    return (lrange.stop + rrange.start)//2

def solve(filename):
    range_list = list()
    candidates = list()
    with open(filename) as infile:
        for line in infile.readlines():
            l = line.strip()
            if '-' in l:
                left, right = l.split('-')
                range_list.append(Crange(int(left), int(right)+1))
            elif l:
                candidates.append(int(l))

    range_list.sort()
    i = 0
    while i < len(range_list)-1:
        if range_list[i].intersects(range_list[i+1]):
            range_list[i] += range_list[i+1]
            del(range_list[i+1])
            continue
        i += 1

    node = RangeTree(range_list)
    count = sum([c in node for c in candidates])
    nitems = sum([len(r) for r in range_list])
    return count, nitems
    

if __name__=='__main__':
    t = timeit.timeit(lambda: solve('test.txt'), number=1000)
    t += timeit.timeit(lambda: solve('input.txt'), number=1000)
    print(f"took {t}s")
    count, nitems = solve('test.txt')
    print(f"test.txt: There are {count} fresh ingredients")
    print(f"test.txt: There are {nitems} items")
    count, nitems = solve('input.txt')
    print(f"input.txt: There are {count} fresh ingredients")
    print(f"input.txt: There are {nitems} items")
