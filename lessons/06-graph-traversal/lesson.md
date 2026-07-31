# Graph Traversal — DFS & BFS

A graph is nodes joined by edges; grids and matrices are graphs in disguise (each
cell is a node linked to its neighbours). Two traversals cover most of it.

## DFS vs BFS

- **DFS** goes deep before wide — natural via recursion or a stack. Great for
  connectivity, flood-fill, counting components, and cycle detection.
- **BFS** expands in rings from the source using a **queue** — and on an
  **unweighted** graph it finds the **shortest path** (fewest edges).

## The core patterns

```python
# BFS shortest path (unweighted)
from collections import deque
q, seen = deque([(start, 0)]), {start}
while q:
    node, dist = q.popleft()
    if node == goal:
        return dist
    for nxt in neighbours(node):
        if nxt not in seen:
            seen.add(nxt)
            q.append((nxt, dist + 1))

# DFS flood-fill on a grid
def dfs(r, c):
    if out_of_bounds(r, c) or grid[r][c] != target or (r, c) in seen:
        return
    seen.add((r, c))
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        dfs(r + dr, c + dc)
```

## The essentials

Always keep a **visited** set — without it you'll loop forever on cycles. Decide
neighbours carefully (4- vs 8-directional on grids). Reach for **BFS when you need
the shortest number of steps**, DFS when you just need to explore or count.
