
def generate_adjacent(M,N,m,n):
    for mi in range(m-1, m+2):
        for ni in range(n-1, n+2):
            if mi in range(0,M) and ni in range(0,N) and (mi,ni) != (m,n):
                yield mi, ni

def solve_a(filename):
    with open(filename) as file:
        lines = [l.strip() for l in file.readlines()]

    M = len(lines)
    N = len(lines[0])

    _map = []
    for m in range(M):
        _map.append([0]*N)
        for n in range(N):
            if lines[m][n] == '@':
                _map[m][n] = 1

    forklift_positions = 0
    for m in range(M):
        for n in range(N):
            if _map[m][n] == 1:
                count_rolls = 0
                for mn,nn in generate_adjacent(M,N,m,n):
                    count_rolls += _map[mn][nn]
                if count_rolls < 4:
                    forklift_positions += 1

    print(f"A: {filename}: {forklift_positions} positions")


def solve_b(filename):
    with open(filename) as file:
        lines = [l.strip() for l in file.readlines()]

    M = len(lines)
    N = len(lines[0])

    _map = set()
    for m in range(M):
        for n in range(N):
            if lines[m][n] == '@':
                _map.add((m,n))

    count_removed_rolls = 0
    last_map_size = 0
    while len(_map) != last_map_size:
        last_map_size = len(_map)
        accessible_rolls = set()
        for (m,n) in _map:
            count_rolls = 0
            count_rolls = sum([1 for mn,nn in generate_adjacent(M,N,m,n) if (mn,nn) in _map])
            for mn,nn in generate_adjacent(M,N,m,n):
                if (mn,nn) in _map:
                    count_rolls += 1
            if count_rolls < 4:
                accessible_rolls.add((m,n))
        print(f"Removing {len(accessible_rolls)} rolls")
        count_removed_rolls += len(accessible_rolls)
        _map = _map - accessible_rolls

    print(f"B: {filename}: {count_removed_rolls} positions")

solve_a('test.txt')
solve_a('input.txt')

solve_b('test.txt')
solve_b('input.txt')