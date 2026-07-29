import unittest


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
