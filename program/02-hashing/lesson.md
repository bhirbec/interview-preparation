# Hashing

A hash table (Python `dict`/`set`) trades memory for speed: **O(1)** average
insert, lookup, and delete. Most "can you do this faster than O(n²)?" questions
are really "what should I store in a hash map?".

## When to reach for it

- **Membership / dedup** — "have I seen this before?" → a `set`.
- **Counting / frequency** — tally occurrences → a `dict` or `collections.Counter`.
- **Grouping** — bucket items by a key (e.g. anagrams by their sorted letters).
- **Complement lookups** — for each element, check if `target - x` was already
  seen (the classic two-sum trick).

## The core patterns

```python
# Complement lookup — one pass, O(n)
seen = {}
for i, x in enumerate(nums):
    if target - x in seen:
        return (seen[target - x], i)
    seen[x] = i

# Frequency map
from collections import Counter
counts = Counter(s)

# Group by a canonical key
from collections import defaultdict
groups = defaultdict(list)
for w in words:
    groups[tuple(sorted(w))].append(w)
```

## Trade-offs

Hashing removes a loop but costs O(n) extra space, and worst-case lookups degrade
if keys collide badly (rare in practice). Pick a **canonical key** that makes
equal-but-different inputs collapse to the same bucket. Try the exercises.
