# Topological Sort

A topological sort orders the nodes of a **directed acyclic graph (DAG)** so that
every edge `a -> b` puts `a` before `b`. It answers "in what order can I do these
tasks given their dependencies?" — build orders, course schedules, package installs.

## Two standard algorithms

**Kahn's algorithm (BFS on in-degrees)** — the natural iterative one:

```python
from collections import deque
indeg = {n: 0 for n in nodes}
for a, b in edges:            # a must come before b
    indeg[b] += 1
ready = deque(n for n in nodes if indeg[n] == 0)
order = []
while ready:
    n = ready.popleft()
    order.append(n)
    for m in successors[n]:
        indeg[m] -= 1
        if indeg[m] == 0:
            ready.append(m)
# if len(order) < len(nodes): a cycle exists -> no valid order
```

**DFS post-order** — record each node *after* visiting all its successors, then
reverse; use a "visiting" (gray) set to detect cycles.

## The key insight

A node is safe to emit once it has **no unmet prerequisites** (in-degree 0). If
some nodes never reach in-degree 0, the graph has a **cycle** and no ordering
exists — always handle that case.
