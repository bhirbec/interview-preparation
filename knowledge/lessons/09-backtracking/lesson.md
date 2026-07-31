# Backtracking

Backtracking builds candidates incrementally and **abandons a partial candidate
the moment it can't lead to a valid solution**. It's a depth-first search over the
space of choices, undoing each choice as you return.

## When to reach for it

- You must enumerate **all** solutions — subsets, permutations, combinations,
  valid arrangements.
- You're placing/choosing items under constraints (N-queens, sudoku, word search).
- The problem says "generate every…" or "count the ways to…" with structure.

## The core template

```python
def backtrack(path, choices):
    if is_complete(path):
        results.append(path[:])      # copy — path is mutated in place
        return
    for choice in choices:
        if not valid(path, choice):
            continue
        path.append(choice)          # choose
        backtrack(path, next_choices(choices, choice))
        path.pop()                   # un-choose (backtrack)
```

## Making it fast

The naive tree is exponential, so **prune early**: skip a branch as soon as it
violates a constraint rather than checking only complete candidates. Order choices
to fail fast. The exercises — power set, permutations, balanced parens, grid word
search, and eight queens — drill the choose / recurse / un-choose rhythm.
