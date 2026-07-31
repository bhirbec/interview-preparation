# Stacks & Queues

Two disciplines for deferred work: a **stack** is LIFO (last in, first out), a
**queue** is FIFO (first in, first out). In Python: a `list` with
`append`/`pop()` is a stack; `collections.deque` with `append`/`popleft` is a
queue (never `list.pop(0)` — that's O(n)).

## When a stack

- **Nesting & matching** — brackets, parser states, undo histories. Push
  openers; on a closer, the top of the stack must be its partner.
- **Most-recent-first** processing — DFS iteratively, backtracking manually.

```python
PAIRS = {")": "(", "]": "[", "}": "{"}
def valid(s):
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in PAIRS:
            if not stack or stack.pop() != PAIRS[ch]:
                return False
    return not stack
```

## When a queue

- **Order-preserving scheduling** — process tasks in arrival order, re-enqueue
  or delay the ones that aren't ready (cooldowns, round-robin).
- **BFS** — the queue *is* the algorithm.

## The essentials

The stack's invariant is the interview answer: at any point it holds exactly
the *unmatched* openers. Always ask "what does my stack/queue contain, in one
sentence?" — if you can't answer, the design is wrong. Check the empty-stack
pop and the leftover-items-at-end cases.
