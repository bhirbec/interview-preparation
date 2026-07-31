# Bit Manipulation

An integer is a vector of bits, and the bitwise operators — `&` (AND), `|`
(OR), `^` (XOR), `~` (NOT), `<<`/`>>` (shifts) — operate on all of them at
once. A handful of idioms covers nearly every interview question.

## The core idioms

```python
x & 1              # lowest bit — odd/even test
x >> k & 1         # read bit k
x | (1 << k)       # set bit k
x & ~(1 << k)      # clear bit k
x & (x - 1)        # drop the lowest set bit (popcount loop, power-of-2 test)
bin(x).count("1")  # popcount in Python
```

Masks select bit ranges: to splice b into a at positions j..i, **clear** that
window in a with a mask of 0s, shift b left by i, then OR them together.

## XOR — the interview star

`x ^ x = 0`, `x ^ 0 = x`, XOR is order-independent — so XOR-ing a whole array
cancels every pair (find the single unpaired number). XOR is also "add without
carry": full addition is `carry = (a & b) << 1; a = a ^ b` repeated until the
carry dies — that's how you add without `+`.

## A set in an integer

A bitmask encodes a subset: bit i ⇔ element i is in. Iterate all subsets with
`for mask in range(1 << n)`, and use popcount to order or bucket them. This is
also the backbone of bitmask DP.

## The essentials

Python ints are arbitrary-precision: `~x` is `-x-1`, not a 32-bit flip — mask
with `& 0xFFFFFFFF` when a problem assumes fixed width. Precedence trap:
`==` binds tighter than `&`, so parenthesize `(x & 1) == 0`. Say bit positions
out loud (bit 0 = least significant) to avoid off-by-one masks.
