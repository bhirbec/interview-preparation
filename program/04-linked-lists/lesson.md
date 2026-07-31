# Linked Lists

A linked list is a chain of nodes, each holding a value and a pointer to the next.
No random access — but O(1) insertion/deletion once you hold the right node. The
challenge is almost always **pointer bookkeeping**.

## Essential techniques

- **Dummy head**: allocate a throwaway node before the real head so insertion and
  deletion at the front need no special case. Return `dummy.next`.
- **Runner / two pointers**: a `fast` pointer moving twice as fast as `slow` finds
  the middle, detects cycles, or locates the k-th-from-last node in one pass.
- **Reverse by relinking**: flip `next` pointers as you walk, keeping `prev`.

## The core patterns

```python
# Reverse
prev = None
while node:
    node.next_node, prev, node = prev, node, node.next_node
return prev

# Dummy head for safe deletion
dummy = Node(0, head)
prev, cur = dummy, head
while cur:
    if should_delete(cur):
        prev.next_node = cur.next_node
    else:
        prev = cur
    cur = cur.next_node
return dummy.next_node
```

## The traps

Losing the rest of the list by overwriting `next` before saving it; forgetting to
advance a pointer (infinite loop); and edge cases — empty list, single node,
deleting the head or tail. Draw the pointers on paper first. Start below.
