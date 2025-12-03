def test_number_a(num):
    numstr = str(num)
    length = len(numstr)
    divisors = [i for i in range(2, length + 1) if length % i == 0]
    # Part A only for divisor 2 if it is a valid divisor
    divisors = [2] if 2 in divisors else []
    for div in divisors:
        testlength = length // div
        teststr = numstr[:testlength]*div
        yield int(teststr)

def test_number_b(num):
    numstr = str(num)
    length = len(numstr)
    divisors = [i for i in range(2, length + 1) if length % i == 0]
    # Part A only for divisor 2 if it is a valid divisor
    divisors = [d for d in divisors if d > 2]
    for div in divisors:
        testlength = length // div
        teststr = numstr[:testlength]*div
        yield int(teststr)

def test_range(_range):
    invalid_ids_a = set()
    invalid_ids_b = set()
    for num in _range:
        for testnum in test_number_a(num):
            if testnum in _range:
                invalid_ids_a.add(testnum)
        for testnum in test_number_b(num):
            if testnum in _range:
                invalid_ids_b.add(testnum)

    return sum(invalid_ids_a), sum(invalid_ids_a.union(invalid_ids_b))

def solve(filename):
    with open(filename) as infile:
        lines = infile.readlines()
    line = ''.join([l.strip() for l in lines])
    range_pairs = line.split(',')
    ranges = [range(int(l0), int(l1) + 1) for l0, l1 in (pair.split('-') for pair in range_pairs)]

    total_invalid_sum_a = 0
    total_invalid_sum_b = 0
    for _range in ranges:
        isa, isb = test_range(_range)
        print(f"Range {_range} has invalid sum a {isa}")
        print(f"Range {_range} has invalid sum b {isb}")
        total_invalid_sum_a += isa
        total_invalid_sum_b += isb

    print(f"{filename}: Total invalid sum A: {total_invalid_sum_a}")
    print(f"{filename}: Total invalid sum B: {total_invalid_sum_b}")

if __name__ == '__main__':
    solve('test.txt')
    solve('input.txt')


    

