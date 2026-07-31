# Heaps & Priority Queues

A heap is a partially-ordered tree stored in an array: the smallest element is
always at the root, and push/pop cost **O(log n)**. It's the structure for
"repeatedly give me the smallest (or largest) thing" — without keeping
everything fully sorted.

## Python's heapq

`heapq` is a **min-heap** over a plain list. Push tuples to sort by a key; for
a max-heap, negate the key.

```python
import heapq

h = []
heapq.heappush(h, (priority, item))
priority, item = heapq.heappop(h)
```

## The k-way merge pattern

To merge m sorted sequences: seed the heap with each sequence's head, then
repeatedly pop the smallest and push that sequence's next element. Every element
passes through the heap once → **O(N log m)**.

```python
h = [(seq[0], i, 0) for i, seq in enumerate(seqs) if seq]
heapq.heapify(h)
out = []
while h:
    val, i, j = heapq.heappop(h)
    out.append(val)
    if j + 1 < len(seqs[i]):
        heapq.heappush(h, (seqs[i][j + 1], i, j + 1))
```

## Other tells

"k largest / k smallest / k closest" → a heap of size k (O(n log k), better
than sorting). "Continuously take the cheapest option" → a priority queue —
that's also the engine inside Dijkstra's algorithm.

## The essentials

Include a tiebreaker (like the index) in pushed tuples so comparison never
falls through to non-comparable items. `heapify` is O(n) — cheaper than n
pushes. Know the array trick: children of `i` live at `2i+1`, `2i+2`.
