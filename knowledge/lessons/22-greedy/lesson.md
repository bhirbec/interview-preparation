# Greedy

A greedy algorithm makes the **locally best choice at each step** and never
reconsiders. When it's valid it beats DP hands down — one pass, no table. The
whole game is knowing *when* it's valid.

## When greedy works

You need an **exchange argument**: any optimal solution can be reshaped, step
by step, to agree with the greedy choice without getting worse. Classic safe
cases: interval scheduling by earliest end time, fitting the most words on a
line, Huffman merging, taking the largest feasible piece when pieces don't
interact.

```python
# Greedy word wrap: put each word on the current line if it fits
lines, cur = [], ""
for w in words:
    if not cur:
        cur = w
    elif len(cur) + 1 + len(w) <= width:
        cur += " " + w
    else:
        lines.append(cur)
        cur = w
if cur:
    lines.append(cur)
```

## When greedy fails

Coin change with coins {1, 3, 4} and target 6: greedy takes 4+1+1, optimal is
3+3. When a local choice can block better combinations later, you need DP.
**Test your greedy on small adversarial inputs before trusting it.**

## Greedy inside other algorithms

Dijkstra (expand the cheapest node), Kruskal/Prim (cheapest safe edge), and
best-first orderings are greedy strategies wearing algorithm costumes — the
priority queue is greed made efficient.

## The essentials

In an interview, *say the justification*: "greedy works here because …
(exchange argument)". If you can't finish that sentence, sketch the DP instead.
Sorting the input by the right key is usually step one of a greedy solution.
