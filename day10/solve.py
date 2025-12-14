import re
from heapq import heappush, heappop

filename = 'test.txt'

class MachineA:
    def __init__(self, target, buttons, joltage):
        self.state = 0
        self.count = 0
        self.target = target
        self.buttons = buttons
        self.joltage = joltage
    def press(self, n):
        self.state ^= self.buttons[n]
        self.count = self.count + 1
    def get_children(self):
        for n in range(len(self.buttons)):
            nm = MachineA(self.target,self.buttons,self.joltage)
            nm.state = self.state
            nm.count = self.count
            nm.press(n)
            yield nm
    def __repr__(self):
        return str(self.target)
    def __lt__(self, other):
        return self.count < other.count

class MachineB:
    def __init__(self, buttons, joltage):
        self.state = [0 for j in joltage]
        self.count = 0
        self.buttons = buttons
        self.joltage = joltage
    def press(self, n):
        button = self.buttons[n]
        for i,j in enumerate(self.joltage):
            revn = len(self.joltage)-i-1
            if button & (1<<revn):
                self.state[i] += 1
        self.count += 1
    def done(self):
        return all([s==j for s,j in zip(self.state,self.joltage)])
    def can_continue(self):
        return any([s<j for s,j in zip(self.state,self.joltage)])
    def state_done(self, state):
        return all([s==j for s,j in zip(state,self.joltage)])
    def state_can_continue(self, state):
        return all([s<=j for s,j in zip(state,self.joltage)])
    def state_distance(self, state):
        return sum((j-i)**2 for i,j in zip(state, self.joltage))
    def state_min_distance(self, state):
        mdist = 0
        for i,j in zip(state,self.joltage):
            mdist = max(0, j-i)
        return mdist
    def get_children(self):
        for n in range(len(self.buttons)):
            nm = MachineB(self.buttons,self.joltage)
            nm.state = [s for s in self.state]
            nm.count = self.count
            nm.press(n)
            yield nm
    def yield_children(self, count, state):
        for n in range(len(self.buttons)):
            self.count = count
            self.state = [s for s in state]
            self.press(n)
            yield self.count, self.state
    def __repr__(self):
        return str(f"{self.state} of {self.joltage}")
    def __lt__(self, other):
        return self.distance() < other.distance()
    def __hash__(self):
        return hash(tuple(self.state+self.joltage))
    def distance(self):
        return sum((i-j)**2 for i,j in zip(self.state, self.joltage))
            

re_target = re.compile(r"\[(.*)\]")
re_button = re.compile(r"\(([\d,]+)\)")
re_jolt = re.compile(r"{(.*)}")

def solve(filename):
    amachines = list()
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
            print()
            amachines.append(MachineA(numtarget,button_mods,joltage))
            bmachines.append(MachineB(button_mods,joltage))

    TOTSUM = 0
    for m in amachines[:0]:
        MLIST = []
        heappush(MLIST, m)
    
        BEST = float('inf')
        while len(MLIST) > 0:
            m = heappop(MLIST)
            children = m.get_children()
            for c in children:
                if c.state == c.target:
                    if c.count < BEST:
                        BEST = c.count
                elif c.count < BEST:
                    heappush(MLIST, c)
        print(m)
        print(f"{m}: {BEST}")
        TOTSUM += BEST

    print(TOTSUM)

    TOTSUM = 0
    for im,m in enumerate(bmachines):
        DICT = dict()
        MLIST = []

        heappush(MLIST, (m.distance(), m.count, m.state))
    
        BEST = float('inf')
        itcount = 0
        while len(MLIST) > 0:
            itcount += 1
            dist, count, state = heappop(MLIST) 

            astardist = count + m.state_min_distance(state)
            if astardist >= BEST:
                continue

            s = tuple(state)
            if s in DICT:
                if DICT[s] <= count:
                    continue
            DICT[s] = count

            if m.state_done(state):
                BEST = ccount
            elif m.state_can_continue(state):
                for ccount, cstate in m.yield_children(count, state):
                    if m.state_can_continue(cstate):
                        childstartdist = ccount + m.state_min_distance(cstate)
                        if childstartdist < BEST:
                            heappush(MLIST, (m.state_distance(cstate), ccount, cstate))

            
                
                

        print(f"{m}: {BEST} took {itcount}")
        TOTSUM += BEST

    print(TOTSUM)

        





if __name__ == '__main__':
    solve('test.txt')
    solve('input.txt')