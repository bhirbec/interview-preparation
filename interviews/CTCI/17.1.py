
def main():
    for i in xrange(1000):
        for j in xrange(15000):
            if add(i, j) != (i + j):
                print 'problem'
    print '=)'

def add(a, b):
    # TODO: doesn't work with negative value
    xor_val = a ^ b
    and_val = (a & b) << 1
    if xor_val & and_val == 0:
        return xor_val | and_val
    return add(xor_val, and_val)

if __name__ == '__main__':
    main()
