def multiply(a, b):
  if b == 0:
    return 0
  if b == 1:
    return a

  s = multiply(a, b >> 1) << 1
  if b & 1:
    s += a

  return s
