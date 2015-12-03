# There are two sorted arrays A and B both of size n. Find the median
# of the two sorted arrays. The overall run time complexity should
# be O(log(n)).

import random


def main():
    a = random_sorted_array(101)
    b = random_sorted_array(101)
    print median_naive(a, b)
    print median_merge(a, b)
    print median_recursive(a, b)

def median_naive(a, b):
    return sorted(a + b)[len(a)]

def median_merge(a, b):
    n = len(a)
    i, j = 0, 0

    while i + j <= n:
        if j == n or (i < n and a[i] < b[j]):
            med = a[i]
            i += 1
        else:
            med = b[j]
            j += 1

    return med

# Find the median in O(log(n)) time
def median_recursive(a, b):
    return _median(a, b, 0, 0, len(a))

def _median(a, b, start1, start2, n):
    if n == 1:
        return max(a[start1], b[start2])

    l = n / 2
    m1 = start1 + l
    m2 = start2 + l
    med1 = a[m1]
    med2 = b[m2]

    if med1 == med2:
        return med1

    if med1 < med2:
        start1 = m1
    else:
        start2 = m2

    if n % 2 == 1:
        l += 1

    return _median(a, b, start1, start2, l)

def random_sorted_array(n):
    array = [int(random.uniform(0, n)) for i in range(n)]
    array.sort()
    return array

main()
