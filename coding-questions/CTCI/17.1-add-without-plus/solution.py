MASK = 0xFFFFFFFF
INT_MAX = 0x7FFFFFFF


def add(a, b):
  a &= MASK
  b &= MASK
  while b != 0:
    carry = (a & b) << 1
    a = (a ^ b) & MASK
    b = carry & MASK
  # Reinterpret the 32-bit result as a signed two's-complement integer.
  return a if a <= INT_MAX else a - (MASK + 1)
