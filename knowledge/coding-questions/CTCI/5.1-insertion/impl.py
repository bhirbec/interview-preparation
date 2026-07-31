# Insertion
#
# You are given two 32-bit numbers, n and m, and two bit positions i and j
# (with i <= j). Insert m into n so that m occupies bits j through i of n. You
# can assume that bits j through i have enough room to fit all of m; that is, if
# m = 10011, it could be inserted at positions j = 6 and i = 2, but not at
# positions j = 5 and i = 2 (there would be no room to fit m starting at bit 2).
# Return the resulting number.
#
# Examples:
#   insert_bits(n=0b10000000000, m=0b10011, i=2, j=6) -> 0b10001001100  (1100)
#   insert_bits(n=161, m=5, i=2, j=4)                 -> 181
#   insert_bits(n=0, m=0b111, i=0, j=2)               -> 7
#   insert_bits(n=0b11111111, m=0, i=2, j=4)          -> 0b11100011 (227)


def insert_bits(n, m, i, j):
  # TODO: implement
  raise NotImplementedError
