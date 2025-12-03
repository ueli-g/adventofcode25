def solve(filename, search_len):
    with open(filename) as infile:
        lines = [l.strip() for l in infile.readlines()]

        total_sum = 0

        for line in lines:
            candidate = line[-search_len:]
            reverse_iterator = len(line) - search_len - 1
            while reverse_iterator >= 0:
                if line[reverse_iterator] >= candidate[0]:
                    carry = line[reverse_iterator]
                    for forward_iterator in range(search_len):
                        if carry >= candidate[forward_iterator]:
                            next_carry = candidate[forward_iterator]
                            candidate = candidate[:forward_iterator] + carry + candidate[forward_iterator+1:]
                            carry = next_carry
                        else:
                            carry = str(0)
                reverse_iterator -= 1
            total_sum += int(candidate)

        print(f"Final value for {filename}: {total_sum}")

solve('test.txt', 2)
solve('input.txt', 2)

solve('test.txt', 12)
solve('input.txt', 12)
