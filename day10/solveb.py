import re
from heapq import heappush, heappop

filename = 'test.txt'

def count_bits(b):
    count = 0
    while b > 0:
        count += b&1
        b = b>>1
    return count

class MachineB:
    def __init__(self, buttons, joltage):
        self.state = joltage
        self.count = 0
        for b in buttons:
            lengths = [count_bits(b) for b in buttons]
        lengthsort, bsort = zip(*sorted(zip(lengths, buttons)))
        self.lengths = lengthsort[::-1]
        self.buttons = bsort[::-1]

    def state_press(self, state, n):
        button = self.buttons[n]
        state_len = len(state)
        for i in range(state_len):
            revn = state_len - i - 1
            if button & (1<<revn):
                state[i] -= 1

    def state_done(self, state):
        return all([s==0 for s in state])

    def state_can_continue(self, state):
        return all([s>=0 for s in state])

    def state_distance(self, state):
        return sum(s**2 for s in state)

    def state_min_distance(self, dim, state):
        
        if dim == len(self.buttons):
            return float('inf')
        
        button = 0
        for b in self.buttons[dim:]:
            button = button | b

        stateiter = state
        for s in state[::-1]:
            if s > 0 and not (button & 1):
                return float('inf')
            button = button >> 1

        return sum(state)/self.lengths[dim]

    def state_opt_distance(self, state):
        return max(state)

    def yield_children(self, b_start_dim, count, state):
        n = b_start_dim
        if n >= len(self.buttons):
            return

        yield n+1, count, state[:]

        newcount = count
        #oldstate = state[:]
        newstate = state[:]

        self.state_press(newstate, n)
        while self.state_can_continue(newstate):
            newcount += 1
            yield n + 1, newcount, newstate
            newstate = newstate[:]
            self.state_press(newstate, n)
        else:
            newcount -= 1


        #yield newcount, oldstate

    def __repr__(self):
        return str(f"{self.state}")

    def __lt__(self, other):
        return self.distance() < other.distance()

    def __hash__(self):
        return hash(tuple(self.state))

    def distance(self):
        return sum((i-j)**2 for i,j in zip(self.state, self.joltage))
            

re_target = re.compile(r"\[(.*)\]")
re_button = re.compile(r"\(([\d,]+)\)")
re_jolt = re.compile(r"{(.*)}")

def solve_machine(im, m):
    TOTSUM = 0
    DICT = dict()
    MLIST = []

    state = m.state
    count = 0
    startdim = 0
    dist = m.state_distance(state)

    heappush(MLIST, (dist, startdim, count, state))

    WORSTCOST = sum(state)/m.lengths[-1]

    BEST = WORSTCOST
    BESTASTAR = WORSTCOST

    itcount = 0
    while len(MLIST) > 0:
        itcount += 1
        dist, dim, count, state = heappop(MLIST)

        

        print(f"{im}: exploring cost {count} for {state}")

        if count >= BEST:
            continue

        astardist = count + m.state_min_distance(dim, state)
        if astardist >= BEST:
            continue

        s = tuple(state+[dim])
        if astardist > DICT.get(s, BEST):
            continue
        DICT[s] = astardist
        
        if m.state_done(state):
            if count < BEST:
                BEST = count
        elif m.state_can_continue(state):
            for bdim, ccount, cstate in m.yield_children(dim, count, state):
                if ccount < count:
                    print()
                if m.state_done(cstate):
                    if ccount < BEST:
                        BEST = ccount
                elif m.state_can_continue(cstate):
                    opt_dist = ccount + m.state_min_distance(bdim, cstate)                            
                    s = tuple(cstate+[bdim])
                    if opt_dist < DICT.get(s, BEST):
                        DICT[s] = opt_dist
                        heappush(MLIST, (opt_dist, bdim, ccount, cstate))
        else:
            print()
    print(f"{m}: {BEST} took {itcount}")
    TOTSUM += BEST
    return TOTSUM



def solve(filename):
    bmachines = list()
    with open(filename) as infile:
        lines = [l.strip() for l in infile.readlines()]
        for line in lines:
            if target := re_target.match(line):
                targets = target.group(1)
                numtarget = 0
                for i,c in enumerate(targets[::-1]):
                    numtarget = numtarget | ((c=='#') << i)
            button_mods = []
            for button in re_button.findall(line):
                button_mod = 0
                for pos in button.split(','):
                    button_mod = button_mod | (1 << (i-int(pos)))
                button_mods.append(button_mod)
            for joltage in re_jolt.findall(line):
                joltage = [int(j) for j in joltage.split(',')]
            bmachines.append(MachineB(button_mods,joltage))

    totsum = 0
    for im,m in enumerate(bmachines):
        totsum += solve_machine(im,m)
        
    print(totsum)

if __name__ == '__main__':
    solve('test.txt')
    solve('input.txt')