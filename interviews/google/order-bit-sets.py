# https://www.careercup.com/question?id=5726391455711232

# Given k - which is the number of bits, print all the possible combinations of numbers formed
# by printing all numbers with one bit set, followed by two bits set, ... upto the point when
# all k-bits are set. They must be sorted according to the number of bits set, if two numbers
# have the same number of bits set then they should be placed as per their value.

# For example if K=3

# Output:
# 000, 001, 010, 100,101, 110, 011, 111
# 0 bits set, followed by 1 bits set followed by 2 bits set followed by 3 bits set.


from itertools import product

def generate_bits(k):
    for i in range(1, k+1):
        for bits in _generate_combinations(i, k):
            print bits

def _generate_combinations(n, size):
    def _f(bits, i, start, end):
        if i == n:
            yield format_str.format(bits)
            return

        for p in xrange(start, end+1):
            mask = 1 << p
            bits |= mask
            for v in _f(bits, i+1, p+1, end+1):
                yield v
            bits &= ~mask

    format_str = '{0:0%db}' % size
    return _f(0, 0, 0, size-n)


generate_bits(k=8)

def generate_bits_1(k):
    '''
    - compute cartesian product
    - sort the list by counting the number of bits
    '''
    prod = list(product('01', repeat=k))
    prod.sort(key=lambda c: c.count('1'))
    return prod

def generate_bits_2(k):
    def _gosper(n):
        """return smallest number > n with the same number of bits set"""
        # group is first sequence of 1's in n starting from lowest bits
        # 000111110000
        #    ^---^ - this is "group"

        # the idea is simple - take the highest bit in group
        # and move it one position left
        # the rest of the group will go to the right
        # like this:

        # 000111110000
        # turns into
        # 001000001111
        # after another iteration this turns into
        # 001000010111
        # and so forth...

        # lowest_set_bit is the lowest 1 in that group
        # 000111110000
        #        ^ here it is
        lowest_set_bit = ((~n) + 1) & n

        # this points straight before the highest bit
        # 0001110000
        #   ^ here - to the 0
        new_group_head = (lowest_set_bit + n) & (~n)

        # now let's work with what was left on the left
        original_group = n & (new_group_head - 1)
        # remove group old head - it has migrated one bit left
        new_group = original_group ^ (new_group_head / 2)
        # move the tail to the beginning
        new_group /= lowest_set_bit

        # reassemble result
        result = n & ~original_group
        result |= new_group_head
        result |= new_group

        assert result > n
        assert bin(result).count('1') == bin(n).count('1')
        return result

    yield '0' * k
    mask = 1 << k
    for num_bits in xrange(1, k + 1):
        n = (1 << num_bits) - 1
        while n < mask:
            yield bin(n)[2:].rjust(k, '0')
            n = _gosper(n)

def generate_bits_3(k):
    '''
    Time: O(2^k) Space: O(2^k)
    - recursively compute all 2^k combinations from the smallest number to the biggest
    - keep track of the number of bits for each combination
    - store combinations into a vector where the ith position holds all the combinations with i bits set to 1
    '''

    vector = [0 for i in range(k)]

    def _combinations(vector, pos, k, c):
        if pos == k:
            yield c, tuple(vector)
            return

        vector[pos] = 0
        for _c, p in _combinations(vector, pos+1, k, c):
            yield _c, p

        vector[pos] = 1
        for _c, p in _combinations(vector, pos+1, k, c+1):
            yield _c, p

    store = list( [] for i in xrange(k+1) )
    for c, p in _combinations(vector, 0, k, 0):
        store[c].append(p)

    for comb in store:
        for bits in comb:
            yield bits

