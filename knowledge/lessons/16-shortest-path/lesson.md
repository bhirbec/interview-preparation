# Shortest Paths (Dijkstra)

BFS finds shortest paths when every edge costs 1. When edges have **weights**,
the frontier must expand *cheapest-first* instead of nearest-first — swap BFS's
queue for a **priority queue** and you have **Dijkstra's algorithm**.

## The algorithm

Keep the best-known cost to each node. Repeatedly pop the unvisited node with
the smallest cost — that cost is now final — and *relax* its neighbours:

```python
import heapq

def dijkstra(start, neighbours):
    dist = {start: 0}
    h = [(0, start)]
    done = set()
    while h:
        d, node = heapq.heappop(h)
        if node in done:
            continue
        done.add(node)
        for nxt, w in neighbours(node):
            nd = d + w
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                heapq.heappush(h, (nd, nxt))
    return dist
```

O((V + E) log V) with a binary heap. Requires **non-negative** weights — the
greedy "popped means final" claim breaks with negative edges (that's
Bellman-Ford territory).

## Variants worth knowing

- **Minimax / bottleneck paths**: minimize the *maximum* edge on the path
  instead of the sum — same code, but relax with `max(d, w)` instead of `d + w`
  (e.g. "earliest time you can swim across a rising flood").
- **A\***: Dijkstra plus a heuristic lower bound, for spatial grids.

## The essentials

Skip stale heap entries (the `if node in done: continue` guard) — nodes get
pushed multiple times. On a grid, "nodes" are cells and weights come from the
cells' values. If all weights are equal, just use BFS.
