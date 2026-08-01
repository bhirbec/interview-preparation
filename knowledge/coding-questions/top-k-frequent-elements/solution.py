import heapq


def top_k_frequent(nums, k):
  counts = {}
  for n in nums:
    counts[n] = counts.get(n, 0) + 1

  # Min-heap of the k best (value, frequency) pairs so far. The key is
  # (frequency, -value): the weakest candidate under the required ordering
  # (rarest first, then largest value) sits on top and is evicted first.
  heap = []
  for value, freq in counts.items():
    if len(heap) < k:
      heapq.heappush(heap, (freq, -value, value))
    elif (freq, -value) > (heap[0][0], heap[0][1]):
      heapq.heapreplace(heap, (freq, -value, value))

  # The heap is unordered beyond its root, so sort the survivors for output.
  return [value for _, _, value in sorted(heap, key=lambda e: (-e[0], e[2]))]
