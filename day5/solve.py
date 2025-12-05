
import timeit
from heapq import heappush, heappop

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

def place_in_list(_list, _num):
    n2 = len(_list)//2
    if n2 == 0:
        return 0 if _num < _list[0] else 1
    if _num < _list[n2]:
        return place_in_list(_list[:n2], _num)
    else:
        return n2 + place_in_list(_list[n2:], _num)

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
            self.range = ranges[0]

    def __contains__(self, numlist):
        if self.mid == float('inf'):
            return sum(num in self.range for num in numlist)
        else:
            split = place_in_list(numlist, self.mid)
            left = numlist[:split]
            right = numlist[split:]
            ans = 0
            ans += self.children[0].__contains__(left) if left else 0
            ans += self.children[1].__contains__(right) if right else 0 
            return ans

def bisect(lrange, rrange):
    #assert(rrange.start > lrange.stop)
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
                heappush(candidates, int(l))
    
    range_list.sort()
    i = 0
    while i < len(range_list)-1:
        if range_list[i].intersects(range_list[i+1]):
            range_list[i] += range_list[i+1]
            del(range_list[i+1])
            continue
        i += 1

    sorted_candidates = list(heappop(candidates) for c in range(len(candidates)))

    node = RangeTree(range_list)
    count = node.__contains__(sorted_candidates)
    nitems = sum([len(r) for r in range_list])
    return count, nitems
    
if __name__=='__main__':
    count, nitems = solve('test.txt')
    print(f"test.txt: There are {count} fresh ingredients")
    print(f"test.txt: There are {nitems} items")
    count, nitems = solve('input.txt')
    print(f"input.txt: There are {count} fresh ingredients")
    print(f"input.txt: There are {nitems} items")
    t = timeit.timeit(lambda: solve('test.txt'), number=1000)
    t += timeit.timeit(lambda: solve('input.txt'), number=1000)
    print(f"took {t}s")
