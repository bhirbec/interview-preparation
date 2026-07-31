# Strings

Strings are arrays of characters with two extra twists: they're **immutable** in
Python (build results with a list + `join`), and many problems are really about
**character counts** rather than the characters' order.

## The two workhorses

- **Frequency counting** — permutations, anagrams, and "can it be rearranged
  into X" questions never need the actual arrangements; compare `Counter`s.
- **Scanning with state** — compression, run-length encoding, and ordering
  checks are a single pass with a little bookkeeping (current run, last seen).

```python
from collections import Counter

# Are two strings permutations of each other?
def is_permutation(a, b):
    return Counter(a) == Counter(b)

# Run-length compression — build with a list, join once
def compress(s):
    out, run = [], 1
    for i in range(1, len(s) + 1):
        if i < len(s) and s[i] == s[i - 1]:
            run += 1
        else:
            out.append(s[i - 1] + str(run))
            run = 1
    return "".join(out)
```

## Canonical forms

To group or compare strings ignoring order, map each to a **canonical key**:
`sorted(word)` or its `Counter`. Equal keys ⇔ same letters.

## The essentials

`"".join(parts)` beats repeated `+=` (quadratic). Be explicit about case
sensitivity and non-letter characters — say your assumption out loud in an
interview. A permutation can form a palindrome iff **at most one** character has
an odd count.
