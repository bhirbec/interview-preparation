
def main():
    array = [1, 2, 0, -8, 0, 6, 7, 3, 3, -89]
    print(recursive(array))
    print(bottom_up(array))
    print(longuest_increasing_subseq(array))


def recursive(array):
    n = len(array)
    cache = [0] * n

    def _f(i):
        if cache[i] > 0:
            return cache[i]

        length = 1
        for j in range(i):
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

    for i in range(n):
        for j in range(i):
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


def longuest_increasing_subseq(arr):
  n = len(arr)
  sizes = [1] * n
  indexes = [None] * n

  for i in range(1, n):
    for j in range(i):
      if arr[i] >= arr[j]:
        size = sizes[j] + 1
        if size >= sizes[i]:
          sizes[i] = size
          indexes[i] = j

  max_size = 0
  k = None

  for i, size in enumerate(sizes):
    if size >= max_size:
      max_size = size
      k = i

  lis = []
  while k is not None:
    lis.append(arr[k])
    k = indexes[k]

  return list(reversed(lis))


arr = [0, 1, 2, 1, 4, 0]
longuest_increasing_subseq(arr)
main()
