# Google interview found on Glassdoor
# https://www.glassdoor.com/Interview/You-are-given-a-collection-of-M-arrays-with-N-integers-Every-array-is-sorted-Develop-an-algorithm-to-combine-each-array-i-QTN_1195702.htm

# You are given a collection of M sorted arrays with N integers.
# Develop an algorithm to combine each array into one sorted array.

import heapq


def main():
    a1 = [1, 1,  1,  1,  1, 45]
    a2 = [1, 4,  7,  9, 12, 23]
    a3 = [5, 6, 11, 14, 17, 22]
    a4 = [3, 4,  9, 15, 18, 32]
    print merge_naive([a1, a2, a3, a4], 6)
    print merge_with_heap([a1, a2, a3, a4], 6)


def merge_with_heap(arrays, n):
    '''
    Time: O(n * m * log(m))
    Extra space: log(m)
    '''
    m = len(arrays)
    size = n*m
    h = []
    merged = [0]*size

    for i in xrange(m):
        val = arrays[i][0]
        heapq.heappush(h, (val, i, 0))

    for k in xrange(size):
        val, i, j = heapq.heappop(h)
        merged[k] = val

        # array i isn't done
        if j < n-1:
            j += 1
            val = arrays[i][j]
            heapq.heappush(h, (val, i, j))

    return merged

def merge_naive(arrays, n):
    '''
    Merge m arrays of size n into one single array of size n*m.

    Time: O(n * m^2)
    Extra space: O(m)
    '''
    m = len(arrays)
    size = n*m
    mins = [0]*m
    merged = [0]*size

    def _find_min():
        min_val, i, j = None, None, None
        for _i, _j in enumerate(mins):
            if _j < 0:
                continue
            val = arrays[_i][_j]
            if min_val is None or val < min_val:
               min_val, i, j = val, _i, _j

        return min_val, i, j

    for k in xrange(size):
        merged[k], i, j = _find_min()
        if j < n-1:
            mins[i] = j+1
        else:
            mins[i] = -1

    return merged


if __name__ == '__main__':
    main()
