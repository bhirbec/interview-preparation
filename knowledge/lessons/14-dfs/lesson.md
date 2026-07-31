# Depth-First Search (DFS)

A graph is nodes joined by edges — and grids/matrices are graphs in disguise
(each cell is a node linked to its neighbours). **DFS** explores as far as it can
along one path before backtracking, via recursion or an explicit stack.

## When to reach for it

- **Connectivity / reachability** — can you get from A to B?
- **Connected components / flood fill** — label or count separate regions.
- **Cycle detection** and exhaustively visiting everything reachable.

DFS is the tool when you just need to *visit* everything reachable — the order
you visit in and the distance travelled don't matter.

## The core pattern

```python
seen = set()

def dfs(node):
    if node in seen:
        return
    seen.add(node)
    for nxt in neighbours(node):
        dfs(nxt)

# Grid flood-fill — the neighbours are the 4 orthogonal cells
def dfs(r, c):
    if out_of_bounds(r, c) or grid[r][c] != target or (r, c) in seen:
        return
    seen.add((r, c))
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        dfs(r + dr, c + dc)
```

## The essentials

Always keep a **visited** set — without it you loop forever on cycles. Decide
neighbours deliberately (4- vs 8-directional on grids). On very deep graphs
recursion can overflow the call stack — switch to an explicit stack if needed.
Runtime is **O(V + E)**: every node and edge is touched once.
