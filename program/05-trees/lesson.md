# Trees & Binary Search Trees

A binary tree is a recursive structure: every node has a left and right subtree
that are themselves trees. That recursion is your best tool — most tree problems
have a clean **"solve the children, then combine"** shape.

## Traversals

- **DFS** (recursion or an explicit stack): pre-order (node, left, right),
  in-order (left, node, right), post-order (left, right, node). **In-order of a
  BST yields sorted values** — remember that.
- **BFS** (a queue): visit level by level; use it when depth/levels matter.

## The core pattern

```python
def dfs(node):
    if node is None:
        return base_case
    left = dfs(node.left)
    right = dfs(node.right)
    return combine(node.val, left, right)
```

## Binary Search Trees

A BST keeps `left < node < right` **for every node**, so search/insert is
O(h) — O(log n) when balanced. A common bug: validating a BST by only comparing a
node to its immediate children. You must thread a **(low, high) range** down the
recursion so each node respects the bounds set by *all* its ancestors.

The exercises cover construction, level-order, validation, path sums, and subtree
matching.
