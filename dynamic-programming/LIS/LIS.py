# Problem:
# For a vector of size N, find its LIS

# Example:
# D = 3, 2, 6, 4, 5 1
# LIS = 2, 4, 5

# 1.Naive Algo:
# *************

# for i=N; i>0l i-- {
#   find all subsequence of D with length i
#   if there is one subsequence:
#       break
# }

# Time complexity: O(2^N)

# Dynamic Programming Algorithm
# *****************************

# subproblem: we define a vector L such that:
# - L[i] = LIS of D that end with D[i]
# - L[0] = {D[0]}

# D = 3, 2, 6, 4, 5 1
# L[0] = {3}
# L[1] = {2}
# L[2] = {2, 6}
# L[3] = {2, 4}
# L[4] = {2, 4, 5}
# L[5] = {1}

# General formula:
# L[i] = MAX(L[i] | i<j, D[j] < D[i]) + D[i]

# Time Complexity: O(n^2)

def recursive(array):
    def _f(i):
        if i < 0:
            return 0

        if cache[i] > 0:
            return cache[i]

        length = 1
        for j in xrange(i):
            s = _f(j)
            if array[i] >= array[j] and s + 1 > length:
                length = s + 1

        cache[i] = length
        return length

    n = len(array)
    cache = [0]*n
    m = _f(n-1)
    return reconstruct(m, n, cache, array)

def bottom_up(array):
    n = len(array)
    cache = [1] * n

    for i in xrange(n):
        for j in xrange(i):
            if array[i] >= array[j] and cache[j] + 1 > cache[i]:
                cache[i] = cache[j] + 1

    m = max(cache)
    return reconstruct(m, n, cache, array)

def reconstruct(m, n, cache, array):
    i = n - 1
    output = []

    while i > 0:
        if cache[i] == m:
            output.append(array[i])
            m -= 1
        i -= 1

    return list(reversed(output))

array = [1, 2, 0, -8, 0, 6, 7, 3, 3, 89]
print recursive(array)
print bottom_up(array)
