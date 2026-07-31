# Assorted Problems

Not everything fits a named technique — and interviews love that. These
problems test whether you can turn a fuzzy statement into precise rules and
clean code without a pattern to lean on.

## How to attack an unclassified problem

1. **Restate the rules** in your own words, then extract every constraint the
   statement implies but doesn't spell out (ties, boundaries, empty cases).
   Half of these problems are won at this step.
2. **Choose a representation** that makes the rules cheap to check — a grid, a
   set of occupied cells, a vector cross-product for orientation.
3. **Decompose into helpers** with single jobs (`fits(word, row, col)`,
   `same_side(p, a, b)`), then write the orchestration on top.
4. **Walk one example by hand** before running — simulation problems fail on
   rule misreadings far more than on coding slips.

## Geometry survival kit

The cross product's sign tells you which side of line AB point P is on:

```python
def cross(a, b, p):
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
```

A point is inside a triangle iff the three cross products (one per edge, walked
consistently) share a sign. Stick to integer arithmetic — no angles, no floats.

## The essentials

State your assumptions out loud, keep helpers tiny, and test the degenerate
cases first (empty grid, collinear points, zero-area triangle). Clean
decomposition *is* the skill being graded here.
