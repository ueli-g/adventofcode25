
def solve_a(filename):
    beams = set()
    hitcount = 0
    with open(filename) as infile:
        for line in infile.readlines():
            line = line.strip()
            hits = set()
            for n,c in enumerate(line):
                if c == 'S':
                    beams.add(n)
                elif c == '^':
                    if n in beams:
                        hits.add(n)
            hitcount += len(hits)
            for h in hits:
                beams.remove(h)
                beams.add(h - 1)
                beams.add(h + 1)
    return hitcount

def solve_b(filename):
    beamcount = dict()
    worldcount = 1
    with open(filename) as infile:
        for line in infile.readlines():
            line = line.strip()
            hits = set()
            for n,c in enumerate(line):
                if c == 'S':
                    beamcount[n] = 1
                elif c == '^':
                    if beamcount.get(n,0) > 0:
                        hits.add(n)
            for h in hits:
                worldcount += beamcount[h]
                beamcount[h - 1] = beamcount.get(h - 1, 0) + beamcount[h]
                beamcount[h + 1] = beamcount.get(h + 1, 0) + beamcount[h]
                beamcount[h] = 0
    return worldcount

if __name__ == '__main__':
    print(solve_a('test.txt'))
    print(solve_b('test.txt'))
    print(solve_a('input.txt'))
    print(solve_b('input.txt'))