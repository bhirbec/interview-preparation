# Binary Search Trees

A **binary search tree (BST)** is a binary tree with an ordering invariant: for
**every** node, all values in its left subtree are smaller and all values in its
right subtree are larger. That single rule makes search, insert, and delete
**O(h)** — O(log n) when the tree is balanced, O(n) when it degenerates into a
chain.

## Two properties worth memorising

- **In-order traversal yields sorted values.** Walking left → node → right visits
  keys in ascending order — handy for validation, finding the k-th smallest, or
  turning a BST back into a sorted list.
- **Search follows the invariant:** at each node go left if the target is
  smaller, right if larger — you discard half the remaining tree each step, just
  like binary search on an array.

## Validating a BST — the classic trap

The common bug is checking only that each node is between its *immediate*
children. That's not enough — a node must respect the bounds set by **all** its
ancestors. Thread a `(low, high)` range down the recursion:

```python
def is_bst(node, low=float("-inf"), high=float("inf")):
    if node is None:
        return True
    if not (low < node.val < high):
        return False
    return (is_bst(node.left, low, node.val) and
            is_bst(node.right, node.val, high))
```

## Building a balanced BST

From a **sorted** array, the middle element is the root, and the halves on either
side recursively become the left and right subtrees — giving a minimal-height
tree. The exercises cover exactly that construction and the range-based
validation.
