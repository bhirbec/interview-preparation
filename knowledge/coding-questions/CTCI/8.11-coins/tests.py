import unittest


class TestCoins(unittest.TestCase):
  def test_zero(self):
    self.assertEqual(count_repr(0), 1)

  def test_penny_only_amounts(self):
    # Amounts below a nickel can only be made with pennies: exactly one way.
    for n in range(1, 5):
      self.assertEqual(count_repr(n), 1)

  def test_small_known_counts(self):
    self.assertEqual(count_repr(5), 2)
    self.assertEqual(count_repr(6), 2)
    self.assertEqual(count_repr(10), 4)

  def test_canonical_quarter(self):
    self.assertEqual(count_repr(25), 13)

  def test_canonical_hundred(self):
    self.assertEqual(count_repr(100), 242)

  def test_matches_brute_force(self):
    # Independent brute-force count of coin multisets summing to n.
    def brute(n):
      count = 0
      for q in range(n // 25 + 1):
        for d in range((n - 25 * q) // 10 + 1):
          for k in range((n - 25 * q - 10 * d) // 5 + 1):
            rem = n - 25 * q - 10 * d - 5 * k
            if rem >= 0:  # remainder is always payable in pennies
              count += 1
      return count

    for n in range(0, 60):
      self.assertEqual(count_repr(n), brute(n))


if __name__ == '__main__':
  unittest.main()
