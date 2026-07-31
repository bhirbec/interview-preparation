# Dynamic Programming

DP solves a problem by breaking it into **overlapping subproblems** and reusing
their answers instead of recomputing them. If a naive recursion recomputes the
same states, DP is the fix.

## How to spot it

- The problem asks for an **optimum** (max/min/longest/count of ways).
- A solution is built from solutions to **smaller instances** of the same problem.
- The brute-force recursion branches into calls it has already made.

## The recipe

1. **Define the state** — what parameters identify a subproblem? (e.g. `dp[i]` =
   best answer ending at index `i`).
2. **Write the recurrence** — express `dp[state]` from smaller states.
3. **Base cases** — the smallest states.
4. **Order / memoize** — fill bottom-up, or top-down with a cache.

```python
# Top-down memoization
from functools import lru_cache
@lru_cache(None)
def solve(state):
    if base(state):
        return base_value
    return best(solve(s) for s in transitions(state))
```

## Complexity

Runtime ≈ **(number of states) × (work per state)**. Kadane's algorithm,
longest-increasing-subsequence, coin change, and grid paths below each show a
different state design — that framing is the skill worth practising.
