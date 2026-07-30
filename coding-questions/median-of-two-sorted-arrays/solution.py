def find_median(a, b):
  start1 = 0
  start2 = 0
  count = len(a)
  while count > 1:
    half = count // 2
    m1 = start1 + half
    m2 = start2 + half
    if a[m1] == b[m2]:
      return a[m1]
    if a[m1] < b[m2]:
      start1 = m1
    else:
      start2 = m2
    if count % 2 == 1:
      half += 1
    count = half
  return max(a[start1], b[start2])
