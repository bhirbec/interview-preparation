import unittest


class TestCountAbcStrings(unittest.TestCase):
  def test_empty(self):
    self.assertEqual(count_abc_strings(0), 1)

  def test_length_one(self):
    self.assertEqual(count_abc_strings(1), 3)

  def test_length_two_excludes_bb(self):
    self.assertEqual(count_abc_strings(2), 8)

  def test_length_three(self):
    self.assertEqual(count_abc_strings(3), 19)

  def test_length_four(self):
    self.assertEqual(count_abc_strings(4), 43)

  def test_length_five(self):
    self.assertEqual(count_abc_strings(5), 94)

  def test_matches_brute_force(self):
    # Cross-check the recurrence against an exhaustive enumeration.
    from itertools import product

    def brute(n):
      count = 0
      for combo in product('abc', repeat=n):
        s = ''.join(combo)
        if s.count('b') <= 1 and 'ccc' not in s:
          count += 1
      return count

    for n in range(0, 7):
      self.assertEqual(count_abc_strings(n), brute(n))


if __name__ == '__main__':
  unittest.main()
