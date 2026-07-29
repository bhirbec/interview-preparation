# Add Without Plus
# Difficulty: easy
# Tags: #bit-manipulation #math
#
# Add two integers `a` and `b` without using the `+` (or `-`) operator.
# Return their sum.
#
# Input:  two integers a and b (may be negative or zero).
# Output: the integer a + b, computed with bitwise operations only.
#
# Approach: `a ^ b` adds bit positions without carrying; `(a & b) << 1` is the
# carry. Repeat until there is no carry left. Because Python integers are
# unbounded, negatives are handled by masking to 32-bit two's complement so
# the carry terminates and the sign is reconstructed from the top bit.
#
# NOTE: the original implementation only worked for non-negative inputs — with
# a negative operand the carry propagated forever (Python ints never overflow),
# causing infinite recursion. Fixed here with 32-bit masking.
#
# Examples:
#   add(5, 3)   -> 8
#   add(0, 0)   -> 0
#   add(7, 0)   -> 7
#   add(-3, 5)  -> 2
#   add(-4, -6) -> -10


def add(a, b):
  # TODO: implement
  raise NotImplementedError
