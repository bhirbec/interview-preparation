# Recursion Fundamentals

Recursion solves a problem by **trusting a smaller version of itself**. The
discipline: define what the function *promises*, write the smallest case where
the promise is trivially kept, then keep the promise for size n using the
answer for a smaller size — without re-checking how the smaller call works.

## The recipe

1. **Contract** — one sentence: "`solve(n)` returns …".
2. **Base case** — the smallest input, answered directly.
3. **Recursive case** — combine `solve(smaller)` into the answer for `n`.

```python
# Multiply via halving — O(log b) additions
def multiply(a, b):
    if b == 0:
        return 0
    half = multiply(a, b >> 1)
    return half + half + (a if b & 1 else 0)
```

## Divide, delegate, combine

Towers of Hanoi is the purest example: to move n disks, move n-1 aside (trust
the recursion), move the big one, move n-1 back. You never simulate the
sub-moves — the contract handles them. The same "extend a smaller answer"
shape gives uniform shuffles (shuffle n-1 cards, then swap in card n) and
recursive descent over nested structures (JSON trees).

## Recursion vs iteration

Every recursion can become a loop with an explicit stack; use iteration when
depth may exceed Python's ~1000-frame limit. But when the data is recursive
(trees, nested dicts) or the problem statement is self-similar, recursion is
usually the clearer program.

## The essentials

State the base case *first* and make every recursive call strictly smaller —
those two habits eliminate most infinite recursions. If the same subproblem
recurs, you've crossed into dynamic-programming territory: add a cache.
