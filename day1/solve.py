import re


def solve(filename):

    with open(filename, 'r') as file:
        lines = file.readlines()

    pattern = re.compile(r'^(\w)(\d+)')

    dirmap = {
        'L': -1,
        'R': 1,
    }

    clock = 100
    cursor = 50
    zero_counts = 0
    cross_counts = 0

    for line in lines:
        matches = pattern.match(line)
        if matches:
            # Part a
            direction = matches.group(1)
            value = int(matches.group(2))
            last = cursor
            cursor += (dirmap[direction] * value)
            wrapped_cursor = cursor % clock
            if wrapped_cursor == 0:
                zero_counts += 1

            # Part b
            cursor = last + (dirmap[direction] * (value % 100))
            wrapped_cursor = cursor % clock
            extra_laps = value // 100
            cross_counts += extra_laps
            if wrapped_cursor != cursor:
                cross_counts += 1
                if (wrapped_cursor == 0 and direction == 'R') or (last == 0 and direction == 'L'):
                    cross_counts -= 1

            cursor = wrapped_cursor
    cross_counts += zero_counts        
    return zero_counts, cross_counts

print(solve('test.txt'))

print(solve('input.txt'))