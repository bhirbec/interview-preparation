def good_numbers(n):
  if n < 2:
    return []

  counts = [0] * (n + 1)
  a = 1
  while a ** 3 <= n:
    a_cube = a ** 3
    b = a
    while a_cube + b ** 3 <= n:
      counts[a_cube + b ** 3] += 1
      b += 1
    a += 1

  return [t for t, c in enumerate(counts) if c >= 2]
