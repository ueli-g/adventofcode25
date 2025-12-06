import re
import numpy

def solve_a(filename):
    re_nums = re.compile(r'\d+')
    re_ops = re.compile(r'[\+\*]')
    rows = []
    with open(filename) as infile:
        for line in infile.readlines():
            line = line.strip()
            if nums := re_nums.findall(line):
                rows.append([int(n) for n in nums])
            elif ops := re_ops.findall(line):
                rows.append([0 if o == '+' else 1 for o in ops])
                rows.append([int.__add__ if o == '+' else int.__mul__ for o in ops])

    M = len(rows)
    N = len(rows[0])

    for m in range(M-3,-1,-1):
        for n in range(N):
            rows[M-2][n] = rows[M-1][n](rows[M-2][n], rows[m][n])

    print(sum(rows[M-2]))


def solve_b(filename):
    re_num = re.compile(r'\s*(\d+)\s*')
    with open(filename) as infile:
        lines = [l.strip('\n') for l in infile.readlines()]
        M = len(lines)
        N = len(lines[0])
        total_sum = 0
        numlist = []
        for n in range(N-1,-1,-1):
            numstr = ''.join([lines[m][n] for m in range(M)])
            if num := re_num.match(numstr):
                numlist.append(int(num.group(1)))
            if numstr[-1] == '*':
                _prod = 1
                for n in numlist:
                    _prod *= n
                total_sum += _prod
                numlist = []
            elif numstr[-1] == '+':
                _sum = 0
                for n in numlist:
                    _sum += n
                total_sum += _sum
                numlist = []
        print(total_sum)

if __name__ == '__main__':
    solve_a('test.txt')
    solve_b('test.txt')
    solve_a('input.txt')
    solve_b('input.txt')
