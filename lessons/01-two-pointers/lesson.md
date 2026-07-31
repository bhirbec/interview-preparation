# Two Pointers

The two-pointer technique walks a sequence with **two indices** instead of one,
letting you solve in a single pass what would otherwise need a nested loop.

## When to reach for it

- The input is **sorted** (or can be sorted) and you're looking for a pair/triple
  that meets a condition (sum, difference, closeness).
- You need to compare the array from **both ends** inward (palindromes, container
  problems).
- You're maintaining a **sliding window** — a variable-width range `[left, right]`
  that grows and shrinks as you scan.

## The core pattern

```python
left, right = 0, len(arr) - 1
while left < right:
    s = arr[left] + arr[right]
    if s == target:
        return (left, right)
    elif s < target:
        left += 1     # need a bigger sum
    else:
        right -= 1    # need a smaller sum
```

For a sliding window, both pointers move **forward**: advance `right` to include
elements, advance `left` to drop them once a constraint is violated.

## Why it works

Sorting gives you monotonicity: moving a pointer changes the candidate in a known
direction, so you never have to re-examine a discarded position. That turns an
O(n²) search into **O(n)** (plus the sort).

Watch the boundary conditions (`<` vs `<=`), duplicate handling, and integer
overflow. Start with the exercises below.
