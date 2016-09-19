
def main():
    array = [1, 2, 0, -8, 0, 6, 7, 3, 3, -89]
    print recursive(array)
    print bottom_up(array)


def recursive(array):
    n = len(array)
    cache = [0] * n

    def _f(i):
        if cache[i] > 0:
            return cache[i]

        length = 1
        for j in xrange(i):
            s = _f(j)
            if array[i] >= array[j] and s + 1 > length:
                length = s + 1

        cache[i] = length
        return length

    _f(n - 1)
    return reconstruct(array, cache, n)


def bottom_up(array):
    n = len(array)
    cache = [1] * n

    for i in xrange(n):
        for j in xrange(i):
            if array[i] >= array[j] and cache[j] + 1 > cache[i]:
                cache[i] = cache[j] + 1

    return reconstruct(array, cache, n)


def reconstruct(array, cache, n):
    m = max(cache)
    i = n - 1
    output = []

    while i > 0:
        if cache[i] == m:
            output.append(array[i])
            m -= 1
        i -= 1

    return list(reversed(output))

main()
