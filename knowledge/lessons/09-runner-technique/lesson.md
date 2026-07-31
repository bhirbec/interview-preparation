# The Runner Technique

A linked list hides its length and has no random access — but you can walk
**two pointers** through it at different speeds or offsets and learn global
facts in one pass.

## The three classic moves

- **Offset runner** — advance a lead pointer k steps, then move both together;
  when the lead hits the end, the trailer is at the k-th-from-last node.
- **Fast & slow** — fast moves two steps per slow's one: when fast reaches the
  end, slow is at the middle; if the list has a cycle, they *must* meet.
- **Length alignment** — for two lists, compute both lengths, advance the longer
  list's pointer by the difference, then walk in lockstep — the first shared
  node is the intersection.

```python
# k-th to last
lead = trail = head
for _ in range(k):
    lead = lead.next_node
while lead:
    lead, trail = lead.next_node, trail.next_node
return trail
```

## Rebuilding lists

Some problems are easiest by **splitting into sublists** and splicing: keep
separate heads/tails (e.g. a "less than pivot" list and a "greater or equal"
list), append each node to the right one, then connect the tails to heads.

## The essentials

Watch k = 0/1 and lists shorter than k. When splicing sublists, **terminate the
final tail with None** or you'll create a cycle. Intersection is about node
*identity* (`is`), not equal values.
