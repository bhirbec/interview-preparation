def first_bad_version(n, is_bad):
  low, high = 1, n
  while low < high:
    mid = (low + high) // 2
    if is_bad(mid):
      high = mid
    else:
      low = mid + 1
  return low
