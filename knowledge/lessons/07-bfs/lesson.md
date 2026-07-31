# Breadth-First Search (BFS)

**BFS** explores a graph in expanding rings from the source, using a **queue** to
visit every node at distance 1, then distance 2, and so on. Its defining
property: on an **unweighted** graph, the first time BFS reaches a node it has
found the **shortest path** to it (fewest edges).

## When to reach for it

- **Shortest number of steps** between two nodes (unweighted).
- **Multi-source distance**: seed the queue with *every* source at distance 0 to
  compute each cell's distance to the nearest source in one sweep.
- **Level-order** processing, where each ring matters.

## The core pattern

```python
from collections import deque

def bfs(start, goal):
    q, seen = deque([(start, 0)]), {start}
    while q:
        node, dist = q.popleft()
        if node == goal:
            return dist
        for nxt in neighbours(node):
            if nxt not in seen:
                seen.add(nxt)          # mark on ENQUEUE, not on dequeue
                q.append((nxt, dist + 1))
    return -1                          # unreachable
```

Mark a node **when you enqueue** it, not when you pop it — otherwise the same
node gets queued many times and the distances break.

## Beyond unweighted

BFS's shortest-path guarantee holds only when every edge costs the same. When
edges carry **weights**, swap the plain queue for a **priority queue** (min-heap)
and always expand the cheapest-known node — that's **Dijkstra's algorithm**, the
same shape with a heap. Plain BFS runs in **O(V + E)**.
