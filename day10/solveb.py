import re
from heapq import heappush, heappop

filename = 'test.txt'


class MachineB:
    def __init__(self, buttons, joltage):
        self.state = joltage
        self.count = 0
        self.buttons = buttons
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
        return sum(s for s in state)
    def state_min_distance(self, state):
        return max(state)
    def yield_children(self, count, state):
        for n in range(len(self.buttons)):
            count = count
            newstate = [s for s in state]
            self.state_press(newstate, n)
            yield count+1, newstate
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

    TOTSUM = 0
    for m in bmachines:
        DICT = dict()
        MLIST = []

        state = m.state
        count = 0
        dist = m.state_distance(state)

        heappush(MLIST, (dist, count, state))
    
        BEST = float('inf')
        itcount = 0
        while len(MLIST) > 0:
            itcount += 1
            dist, count, state = heappop(MLIST) 

            if m.state_done(state):
                BEST = ccount

            astardist = count + m.state_min_distance(state)
            if astardist >= BEST:
                continue

            #s = tuple(state)
            #if s in DICT:
            #    if DICT[s] <= count:
            #        continue
            #DICT[s] = count

            
            elif m.state_can_continue(state):
                for ccount, cstate in m.yield_children(count, state):
                    if m.state_can_continue(cstate):
                        childstartdist = ccount + m.state_min_distance(cstate)
                        if childstartdist >= BEST:
                            continue
                        s = tuple(cstate)
                        if DICT.get(s, float('inf')) > ccount:
                            DICT[s] = ccount
                            heappush(MLIST, (m.state_distance(cstate), ccount, cstate))

        print(f"{m}: {BEST} took {itcount}")
        TOTSUM += BEST

    print(TOTSUM)

        





if __name__ == '__main__':
    solve('test.txt')
    solve('input.txt')