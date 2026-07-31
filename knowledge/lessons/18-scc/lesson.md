# Strongly Connected Components

In a **directed** graph, node u can be reachable from v while v is unreachable
from u — direction matters. A **strongly connected component (SCC)** is a
maximal set of nodes where every node can reach every other *both ways*.
Collapse each SCC to a single node and the graph becomes a **DAG** (the
condensation) — which is why SCCs show up as a preprocessing step: find the
components, then run DAG algorithms (topological sort, DP) on the condensation.

## Where they appear

- Dependency systems with mutual references (module cycles).
- "Can everyone reach everyone?" / "which parts of this network are
  self-sustaining?"
- 2-SAT solvers, compiler analyses, deadlock detection.

## Kosaraju's algorithm — two DFS passes

1. DFS the graph, pushing each node onto a stack **on exit** (finish order).
2. **Reverse every edge.**
3. Pop nodes off the stack; each DFS in the reversed graph from an unvisited
   node collects exactly one SCC.

```python
def kosaraju(nodes, adj, radj):
    order, seen = [], set()
    def dfs1(u):
        seen.add(u)
        for v in adj[u]:
            if v not in seen:
                dfs1(v)
        order.append(u)                 # exit-time push
    for u in nodes:
        if u not in seen:
            dfs1(u)

    comp, sccs = {}, []
    def dfs2(u, c):
        comp[u] = c
        c.append(u)
        for v in radj[u]:
            if v not in comp:
                dfs2(v, c)
    for u in reversed(order):           # decreasing finish time
        if u not in comp:
            sccs.append([])
            dfs2(u, sccs[-1])
    return sccs
```

Two linear passes → **O(V + E)**. Tarjan's algorithm does it in one pass with
low-link values; know that it exists, but Kosaraju is the one to reproduce
under pressure.

## The essentials

The finish-order + reversed-graph trick works because the *last-finished* node
belongs to a "source" SCC of the condensation, and reversing edges traps the
second DFS inside it. No exercises in the catalog yet — read, then implement
Kosaraju from memory on any directed graph you sketch.
