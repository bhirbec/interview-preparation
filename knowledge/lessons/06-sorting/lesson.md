# Sorting

Know two things about sorting: **how to use it** (constantly) and **how it
works** (for the follow-up questions). Python's `sorted` / `list.sort` is
Timsort — O(n log n), stable.

## Sort as a preprocessing step

Sorting buys you structure: equal elements become adjacent, order becomes
monotonic, and two-pointer/binary-search techniques unlock. "Sort, then scan"
solves a huge family of problems at the cost of O(n log n).

## Custom keys

The `key=` function is where the power is — sort by length, by a canonical
form, by multiple criteria with a tuple:

```python
words.sort(key=len, reverse=True)          # longest first
groups = sorted(words, key=lambda w: "".join(sorted(w)))  # anagram key
items.sort(key=lambda x: (x.priority, -x.size))           # tie-break
```

Stability matters: equal keys keep their original order, so you can sort by a
secondary key first, then by the primary.

## Merging sorted sequences

Two sorted arrays merge in O(n + m) with two pointers — compare heads, take the
smaller. Merging **in place into a buffer** (one array has trailing space) goes
**backwards** from the end so nothing is overwritten before it's read.

## The essentials

Reach for `key=`, never comparator gymnastics. If the interviewer asks for
"faster than O(n log n)", they're hinting at counting sort (small value range)
or a hash map. Know quicksort/mergesort/heapsort trade-offs for the theory
follow-up.
