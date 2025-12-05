
import timeit

class Crange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
    def __contains__(self, other):
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
    def has(self, num):
        return self.start <= num < self.stop

class RangeTree:
    def __init__(self, ranges):
        self.mid = None
        self.range = None
        self.children = ()
        n = len(ranges)
        if n > 1:
            leftranges = ranges[:n//2]
            rightranges = ranges[n//2:]
            self.mid = bisect(leftranges[-1], rightranges[0])
            self.children = (RangeTree(leftranges), RangeTree(rightranges))
        else:
            self.range = ranges[0]
    def __contains__(self, num):
        if self.range:
            return self.range.has(num)
        elif num <= self.mid:
            return num in self.children[0]
        elif num > self.mid:
            return num in self.children[1]

def bisect(lrange, rrange):
    assert(rrange.start > lrange.stop)
    return (lrange.stop + rrange.start)//2

def solve(filename):
    ranges = set()
    candidates = set()

    with open(filename) as infile:
        for line in infile.readlines():
            l = line.strip()
            if '-' in l:
                left, right = l.split('-')
                ranges.add(Crange(int(left), int(right)+1))
            elif l:
                candidates.add(int(l))

    range_list = list(ranges)
    range_list.sort()
    i = 0
    while i < len(range_list)-1:
        if range_list[i+1] in range_list[i]:
            range_list[i] += range_list[i+1]
            del(range_list[i+1])
            continue
        i += 1

    node = RangeTree(range_list)

    count = sum([c in node for c in candidates])
    #print(f"{filename}: There are {count} fresh ingredients")
    nitems = sum([len(r) for r in range_list])
    #print(f"{filename}: There are {nitems} items")

if __name__=='__main__':
    t = timeit.timeit(lambda: solve('test.txt'), number=1000)
    t += timeit.timeit(lambda: solve('input.txt'), number=1000)
    print(f"took {t}")