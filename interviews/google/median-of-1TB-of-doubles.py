# https://www.careercup.com/question?id=5718784741474304

# Alright, the question seems abandoned, so it's safe to post answer:
# IEEE754 doubles have property that if reinterpret_casted to uint64, the comparison will still
# yield correct results (except for negative numbers - how to fix this is exercise to reader)
# Now we interpret doubles as uint64
# So we know total number of doubles in file. Then we count numbers with MSB being 1 and being 0. After
# this is done, we know if median has its MSB as 1 or 0. Then we grep only those numbers that have MSB
# equal to this value and do the same 64 times till we get all bits of median. But hey, we haven't used
# the memory at all. So instead of having 2 counters for 0 and 1 let's have 2^32 counters. This way we
# will be able to find the median in just two passes - once for highest 32 bits and once for lowest 32 bits.
# So we think - there are 1Tb of doubles, that's approximately 140B numbers - we will have to use 37
# bits for every counter (for the worst skew case), and 2**32 * 37 = 158Gib ~ 20 Gb of memory.
# Turns out we are ok with 12 bits for each counter.
# The idea is the following: if some counter overflows, append its number to some list so that later
# we will know that it overflowed. So for k-bit counters we will need k * (2**32) bits for counters
# and 32 * (2**40 / 2 ** k) for overflow entries.

# def mem(k, total = 2 ** 40):
#     bits = k * (2 ** 32) + 32 * total / (2 ** k)
#     return bits / 8

# for i in xrange(1, 100):
#     print i, mem(i) / float(2 ** 30)

# And this gives us 7Gb required memory, so that we have 1Gb for OS runtime , file buffer and etc.
# After we pass through the file, sort the overflow entries (268Millions max) using quicksort and
# merge-sort-step through both arrays in order to get the real uint64_t value of each counter and
# decide where median is.

# So basically this problem is about the bit-bucket trick and counter-compressing trick.

from random import shuffle

SIZE = 6

def main():
    n = 10
    seq = range(100)
    # shuffle(seq)
    numbers = [_int_to_bits(i) for i in seq]

    total = 0
    rank = 3
    prefix = ''

    # for bits in numbers:
    #   print bits

    for pos in range(SIZE):
        count = 0
        for bits in numbers:
            if bits.startswith(prefix) and bits[pos] == '1':
                count += 1

        # print 'pos =', pos, 'total =', total, 'count = ', count, prefix
        if count == 0:
            prefix += '0'
        if total + count > rank:
            prefix += '0'
            total += (n-count)
        elif total + count < rank:
            prefix += '1'
            total += count
        else:
            print 'fu'

    print int(prefix, 2)


def _int_to_bits(number):
    return '{0:b}'.format(number).zfill(SIZE)

main()


