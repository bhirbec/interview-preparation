def count_twos(n):
  if n < 0:
    return 0

  count = 0
  i = 1  # place value of the digit currently being examined
  while i <= n:
    high = n // (i * 10)
    cur = (n // i) % 10
    low = n % i

    if cur < 2:
      count += high * i
    elif cur == 2:
      count += high * i + low + 1
    else:
      count += (high + 1) * i

    i *= 10

  return count
