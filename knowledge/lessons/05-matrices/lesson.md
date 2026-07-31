# Grids & Matrices

A matrix is a list of rows — `grid[r][c]` — and most matrix problems are about
**disciplined index walking**: layer by layer, ring by ring, or cell by cell
with a rule about which cells count.

## Coordinate transforms

In-place rotation and transposition are index mappings, not data shuffles. For a
90° clockwise rotation of an n×n matrix: `(r, c) → (c, n-1-r)`. Rotate four
cells at a time, ring by ring, to do it in place.

## Boundary walks

Spiral orders and ring traversals keep four bounds (`top, bottom, left, right`)
and shrink them as each edge is consumed:

```python
out = []
top, bottom, left, right = 0, n - 1, 0, n - 1
while top <= bottom and left <= right:
    for c in range(left, right + 1):
        out.append(grid[top][c])
    top += 1
    # ... right edge, bottom edge (reversed), left edge (reversed) ...
```

## Column/row dependencies

Some problems make a cell's meaning depend on cells above or beside it (e.g. a
broken machine invalidates everything below it in the column). Scan in the
direction of the dependency and carry per-column/per-row state.

## The essentials

Never mix up `grid[r][c]` vs `grid[c][r]` — name variables `r`/`c`, not `i`/`j`.
Check rectangular vs square assumptions. For in-place work, write the 4-way (or
k-way) swap for **one** cell first, then wrap it in the ring loops.
