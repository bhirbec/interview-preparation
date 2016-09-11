
def print_pairs(n):
    depth = n * 2
    buff = [0] * depth

    def f(n, pos=0, open=0, closed=0):
        if pos == depth:
            print ''.join(buff)
            return

        if open < n:
            buff[pos] = '('
            f(n, pos+1, open+1, closed)

        if open > 0 and closed < open:
            buff[pos] = ')'
            f(n, pos+1, open, closed+1)

    f(n)

print_pairs(n=3)
