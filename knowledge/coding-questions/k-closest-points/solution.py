import heapq


def k_closest(points, k):
  # Max-heap of the k closest points seen so far, keyed on negated squared
  # distance so the farthest of the k sits on top.
  heap = []
  for x, y in points:
    dist = x * x + y * y
    if len(heap) < k:
      heapq.heappush(heap, (-dist, x, y))
    elif -dist > heap[0][0]:
      heapq.heapreplace(heap, (-dist, x, y))
  return [[x, y] for _, x, y in heap]
