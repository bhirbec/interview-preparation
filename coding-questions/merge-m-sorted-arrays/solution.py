import heapq


def merge_sorted_arrays(arrays):
  heap = []
  for i, arr in enumerate(arrays):
    if arr:
      heapq.heappush(heap, (arr[0], i, 0))

  merged = []
  while heap:
    val, i, j = heapq.heappop(heap)
    merged.append(val)
    if j + 1 < len(arrays[i]):
      heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))

  return merged
