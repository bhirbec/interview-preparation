from collections import Counter
from fractions import Fraction
from itertools import combinations


def restore_set(sums):
  m = len(sums)
  n = int((1 + (1 + 8 * m) ** 0.5) / 2)  # m = n*(n-1)/2
  s = sorted(Fraction(x) for x in sums)

  # s[0] = x1+x2 and s[1] = x1+x3; some s[j] is x2+x3, which determines x1.
  for j in range(2, m):
    x1 = (s[0] + s[1] - s[j]) / 2
    xs = [x1, s[0] - x1, s[1] - x1]
    remaining = Counter(s)
    ok = True
    for a, b in combinations(xs, 2):
      if remaining[a + b] > 0:
        remaining[a + b] -= 1
      else:
        ok = False
        break

    while ok and len(xs) < n:
      # The smallest unused sum must involve x1 and the next-smallest value.
      smallest = min(k for k, v in remaining.items() if v > 0)
      nxt = smallest - x1
      for y in xs:
        if remaining[nxt + y] > 0:
          remaining[nxt + y] -= 1
        else:
          ok = False
          break
      if ok:
        xs.append(nxt)

    if ok and len(xs) == n and all(v == 0 for v in remaining.values()):
      return sorted(
          int(x) if x.denominator == 1 else float(x) for x in xs)
  return None  # unreachable for valid input
