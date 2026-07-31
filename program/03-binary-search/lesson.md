# Binary Search

Binary search halves the search space each step, finding an answer in
**O(log n)**. It applies to any **monotonic** predicate — not just sorted arrays.

## When to reach for it

- The data is **sorted** (or rotated-sorted, or virtually sorted).
- You can phrase the question as "find the smallest/largest `x` for which
  `condition(x)` is true", and `condition` flips from false to true exactly once.
- You're searching over an **answer space** (e.g. the minimum capacity that works)
  rather than array indices — "binary search on the answer".

## The core pattern

```python
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = (lo + hi) // 2          # in Python no overflow, but prefer lo+(hi-lo)//2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        lo = mid + 1
    else:
        hi = mid - 1
return -1
```

## The traps

- **Off-by-one**: be deliberate about `lo <= hi` vs `lo < hi`, and whether `mid`
  is inclusive/exclusive when you narrow.
- **Rotation / unknown size**: you may first binary-search for a pivot or an
  upper bound, then search within.
- Always make sure the loop **makes progress** (the range strictly shrinks) so it
  terminates.

The exercises cover rotated arrays, unknown-length arrays, and searching on the
answer.
