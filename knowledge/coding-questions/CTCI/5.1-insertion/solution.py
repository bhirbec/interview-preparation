def insert_bits(n, m, i, j):
  left = (1 << (j + 1)) - 1
  right = (1 << i) - 1
  mask = ~(left ^ right)
  n &= mask
  m = m << i
  return n | m
