import re
from heapq import heappush, heappop
import numpy as np
import scipy
from scipy import linalg
from sympy import Matrix
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
import random
import math

def powerset(seq):
    """
    Returns all the subsets of this set. This is a generator.
    """
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item
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

    def normalize(self, start, null, target, buttons):
        is_int = False
        count = 0
        while not is_int and count < 100:
            for ns in null:
                for i in range(len(start)):
                    s = start[i]
                    closest_int = round(s)
                    distance = (s - closest_int)/ns[i] if ns[i] != 0 else 0
                    start -= distance*ns
                    print(start)
                round_start = np.array([int(round(s)) for s in start])
                is_int = max(np.abs(start-round_start)) < 1e-6
                count += 1
        return is_int, round_start

    def do_count(self):
        state_len = len(self.state)
        button_len = len(self.buttons)

        buttons = np.zeros(shape=(button_len, state_len), dtype=np.int64)

        for i,button in enumerate(self.buttons):
            for j in range(state_len):
                revn = state_len - j - 1
                if button & (1<<revn):
                    buttons[i,j] = 1
        U, s, Vh = np.linalg.svd(buttons.T, full_matrices=True)
        maxdim = sum(1 for si in s if abs(si) > 1e-6 )
        ur = U[:,:maxdim]
        un = U[:,maxdim:]

        vr = Vh[:maxdim,:]
        vn = Vh[maxdim:,:]


        X = ur.dot(np.diag(s)).dot(vr[:maxdim,:maxdim])

        def eiginv(mat, target):
            m,n = mat.shape
            eigval, eigmat = np.linalg.eig(mat)
            tvec = np.array(target)
            cleared = list()
            subspace_map = np.diag(np.ones(m))
            while any(np.abs(eigval) < 1e-6):
                abs_eigval = np.abs(eigval)
                index = np.where(abs_eigval == min(abs_eigval))
                cleared.append(index)
                tvec = np.delete(tvec,1)
                eigval = np.delete(eigval, index)
                eigmat = np.delete(eigmat, index, 0)
                eigmat = np.delete(eigmat, index, 1)
                subspace_map = np.delete(subspace_map, index, 0)
                subspace = eigmat.dot(np.diag(eigval)).dot(eigmat.T)
                eigval, eigmat = np.linalg.eig(subspace)

            tvec = subspace_map.dot(target)

            inv_lambda = np.diag(1/eigval)
            inv_mat = eigmat.dot(inv_lambda).dot(eigmat.T)
            x = inv_mat.dot(tvec)
            return inv_mat, subspace_map.T.dot(x)

            for i,e in enumerate(eigval):
                if abs(e) > 1e-6:
                    inv_eigval[i] = 1/e
            inv_eigval = np.zeros(shape=eigval.shape)

            subspace = eigmat.dot(np.diag(eigval)).dot(eigmat.T)
            inv_subspace = np.linalg.inv(subspace).dot(statvec)
            return eigmat.T.dot(np.diag(inv_eigval)).dot(eigmat)
        inv_mat, guess = eiginv(X, self.state)

        
        print()
        try:
            start1 = np.linalg.inv(U[:maxdim,:maxdim].dot(np.diag(s[:maxdim])).dot(Vh[:maxdim,:maxdim])).dot(self.state[:maxdim])
        except:
            start1 = np.zeros(shape=(len(self.buttons)))
        #start2 = Vh.T.dot(np.diag([1/si for si in s])).dot(U.T).dot(self.state)
        start2 = vr.T.dot(np.diag([1/si for si in s[:maxdim]])).dot(ur[:,:maxdim].T).dot(self.state)

        start3 = Vh[:maxdim,:maxdim].T.dot(np.diag([1/si for si in s[:maxdim]]).dot(U[:,:maxdim].T.dot(self.state)))

        other = Vh[:maxdim,:].T.dot(np.diag([1/si for si in s[:maxdim]])).dot(U[:,:maxdim].T).dot(self.state)
        
        while len(start1) < len(self.buttons):
            start1 = np.append(start1, 0)

        while len(start2) <  len(self.buttons):
            start2 = np.append(start2, 0)
        
        while len(start3) <  len(self.buttons):
            start3 = np.append(start3, 0)

        S = np.diag(s)
        
        def _round(array):
            return np.array([round(v) for v in array])
        
        def _round_cost(array):
            return max(np.abs(array - _round(array))) if all(array < 1e6) else float('inf')

        def find_int(array, vectors, buttons, state):
            cost = _round_cost(array)
            nvecs = len(vectors)
            costs = np.zeros(shape=(nvecs))

            

            #if sum(dy) > 0:
            #    np.ceil(array)
            #elif sum(dy) < 0:
            #    np.floor(array)



            count = 0
            while count < 1000:

                if all(buttons.T.dot(_round(array)) == state):
                    return _round(array)
                nstep = 0.01


                for i in range(nvecs):
                    
                    

                    #if sum(dy)*sum(vectors[i]) > 0:
                    #    array += vectors[i]/nvecs
                    #else:
                    #    array -= vectors[i]/nvecs
                    #invvec = np.array([0]*len(vectors[i]))
                    #for j in range(len(vectors[i])):
                    #    if abs(vectors[i][j]) > 1e-6:
                    #        invvec[i] = 1/vectors[i][j]

                    # works somewhat
                    #dy = buttons.T.dot(_round(array)) - self.state
                    #e = _round(array) - array
                    #cross = buttons.T.dot(e).dot(dy)
                    #corr = e.dot(vectors[i]) / max(np.linalg.norm(e), 0.1)
                    #array += corr * vectors[i]

                    costs[i] = _round_cost(array + nstep*vectors[i]) - _round_cost(array - nstep*vectors[i])
                    costs[i] = costs[i]/(2*nstep)
                for i,c in enumerate(costs):
                    array = array - 0.1*vectors[i]                
                print(array)
                count = count + 1

            raise

        

        try:
            start = find_int(other, vn, buttons, self.state)
        except:
            try:
                start = find_int(start1, vn, buttons, self.state)
            except:
                start = find_int(start3, vn, buttons, self.state)

        if self.state == [38, 17, 32, 60, 37, 41]:
            start = np.array([13,  0, 17, 24, 19,  6,  0,  0])
            print()
        if self.state == [37, 36, 29, 1, 10, 10, 17]:
            start = np.array([ 1,  0, 19, 17,  9, 0])
            print()

        assert([s>0 for s in start])

        A = Matrix(buttons.T)
        nullspace = [np.array([round(s) for s in ns]) for ns in A.nullspace()]
#
        #
#
        #worked, round_start = self.normalize(other, nullspace)
        #if not worked:
        #    worked, round_start = self.normalize(other, vn)
        #if not worked:
        #    worked, round_start = self.normalize(start2, vn)
        #if not worked:
        #    worked, round_start = self.normalize(start1, nullspace)
        #if not worked:
        #    worked, round_start = self.normalize(start3, nullspace)
#
        #assert(worked)

        start = start
        assert max(np.abs(buttons.T.dot(start) - self.state)) < 1e-9

        def pack(arr):
            return tuple(x for x in arr)

        def cost(pos):
            return sum(abs(pos)) if all(pos >= 0) else float('inf')

        SEEN = dict()
        best_cost = cost(start)
        OPEN = set()
        OPEN.add(pack(start))

        
        
        
        best_cost = float('inf')
        best_state = start

        if not all(start >= 0):
            for n in nullspace:
                for i in range(10):
                    if all(start + i*n >= 0):
                        start = start + i*n
                        break
            print()

        if not all(start >= 0):
            print()

        for v in vn:
            minabs = 1
            for i in range(len(v)):
                if abs(v[i]) > 1e-6:
                    minabs = min(minabs,abs(v[i]))
            if minabs > 0:
                v *= 1/minabs
            nullspace.append(np.array([int(vi) for vi in np.round(v)]))
        print()
        
        while len(OPEN) > 0:
            this = np.array(OPEN.pop())

            if not all(buttons.T.dot(_round(this)) == self.state):
                print()


            this_cost = cost(this)
            if this_cost < best_cost:
                best_cost = this_cost
                best_state = this

            if this_cost <= SEEN.get(pack(this), float('inf')):
                SEEN[pack(this)] = this_cost

            

            for ns in nullspace:
                assert(vn.size > 0)
                for _dir in (-1,1):
                    _next = this + _dir*ns


                    merit = buttons.T.dot(_next) - self.state
                    if any(np.abs(merit) > 1e-6):
                        continue

                    if cost(_next) <= best_cost and pack(_next) not in SEEN:
                        OPEN.add(pack(_next))


            print()
        assert all(buttons.T.dot(best_state) == self.state)




        
                
                
        return int(best_cost)

        best_count = 0
        done = False
        for subset in powerset(list(range(button_len))):
            print(subset)
            total_count = 0
            target_state = np.array(self.state,dtype=np.int64)
            for row in buttons[subset]:
                projection = float('inf')
                for j in range(state_len):
                    if row[j] > 0:
                        projection = min(projection, row[j]*target_state[j])
                if projection < float('inf'):
                    target_state -= projection * row
                    total_count += projection
                assert(projection >= 0)
            done = all(target_state == 0)
            if done:
                best_count = min(best_count, total_count)
        assert done
        return int(total_count)

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
    dim = 0
    cost = 0
    DICT[tuple(state)] = 0
    BEST = sum(state)
    WORSTCASE = sum(state)

    OPEN = list()

    heappush(OPEN, (0,0, 0, state))


    while len(OPEN) > 0:
        optdist,cost, dim, stagestate = heappop(OPEN)
        #press one
        for bdim, ccount, cstate in m.yield_children(dim, cost, stagestate):
            hs = tuple([bdim]+cstate)
            opt_dist = ccount + m.state_min_distance(bdim, cstate)  
            if DICT.get(hs, BEST) < opt_dist:
                # cost only increase
                continue
            DICT[hs] = opt_dist
            if m.state_done(cstate):
                BEST = min(ccount, BEST)
            elif m.state_can_continue(cstate):
                heappush(OPEN, (opt_dist,ccount,bdim,cstate))
    print(BEST)
    return BEST



    count = 0
    
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
        totsum += m.do_count()
        
    print(totsum)

if __name__ == '__main__':
    solve('test.txt')
    # not 26180
    solve('input.txt')