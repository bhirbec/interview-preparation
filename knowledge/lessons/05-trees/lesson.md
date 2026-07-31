# Binary Trees

A binary tree is a recursive structure: every node has a left and right subtree
that are themselves trees. That recursion is your best tool — most tree problems
have a clean **"solve the children, then combine"** shape.

## Traversals

- **DFS** (recursion or an explicit stack):
  - **pre-order** — node, left, right (copy/serialize a tree)
  - **in-order** — left, node, right
  - **post-order** — left, right, node (compute a value from the children first)
- **BFS** (a queue): visit level by level; reach for it when depth or per-level
  grouping matters.

## The core pattern

Almost every tree problem is a post-order recursion — get the answer for each
subtree, then combine:

```python
def solve(node):
    if node is None:
        return base_case
    left = solve(node.left)
    right = solve(node.right)
    return combine(node.val, left, right)
```

Height, balanced-ness, subtree sums, node counts, and "does this subtree have
property X" all fit this mould — the trick is choosing what each call **returns**
so the parent can combine cheaply (e.g. return `(height, is_balanced)` in one
pass instead of recomputing height at every node).

## The essentials

Handle the `None` (empty) case first — it's the base case and the source of most
bugs. Prefer a **single post-order pass** that returns everything the parent needs
over repeatedly re-walking subtrees. For level-by-level work, BFS with a queue and
a per-level count is cleaner than tracking depths in a DFS.
