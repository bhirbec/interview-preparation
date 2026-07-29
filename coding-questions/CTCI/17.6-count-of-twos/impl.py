# Count of Twos
# Difficulty: hard
# Tags: #math #recursion
#
# Given a non-negative integer n, count the number of digit `2`s that appear
# across all the integers from 0 to n inclusive. Return that count.
#
# Input:  a non-negative integer n.
# Output: the total number of times the digit 2 occurs in 0, 1, ..., n.
#
# Approach: count the 2s contributed at each digit position independently.
# For a position with place value `i` (1, 10, 100, ...), split n into the
# digits above the position (`high`), the digit at the position (`cur`), and
# the digits below (`low`):
#   - cur < 2  -> high * i twos at this position
#   - cur == 2 -> high * i + low + 1 twos
#   - cur > 2  -> (high + 1) * i twos
# Summing over all positions gives the answer in O(number of digits).
#
# NOTE: the original implementation used an incorrect digit decomposition that
# disagreed with brute force for many inputs (e.g. n = 20 gave 12 instead of
# 3). It has been replaced with the per-position count above; `brut_force`
# below is kept as the reference oracle the tests check against.
#
# Examples:
#   count_twos(2)   -> 1   (just "2")
#   count_twos(20)  -> 3   (2, 12, 20)
#   count_twos(25)  -> 9   (2, 12, and 20..25 each contribute a 2, plus 22 twice)
#   count_twos(100) -> 20

import unittest


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


def brut_force(n):
  s = 0
  for i in range(1, n + 1):
    for c in str(i):
      if c == '2':
        s += 1
  return s


class TestCountTwos(unittest.TestCase):
  def test_small_values(self):
    self.assertEqual(count_twos(0), 0)
    self.assertEqual(count_twos(1), 0)
    self.assertEqual(count_twos(2), 1)
    self.assertEqual(count_twos(20), 3)
    self.assertEqual(count_twos(22), 6)
    self.assertEqual(count_twos(100), 20)

  def test_matches_brute_force(self):
    for n in range(0, 3000):
      self.assertEqual(count_twos(n), brut_force(n), 'mismatch at n=%d' % n)

  def test_larger_value(self):
    self.assertEqual(count_twos(134859), brut_force(134859))


if __name__ == '__main__':
  unittest.main()
