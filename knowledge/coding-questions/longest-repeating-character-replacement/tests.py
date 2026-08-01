import unittest


def brute_force(s, k):
  best = 0
  for i in range(len(s)):
    for j in range(i, len(s)):
      window = s[i:j + 1]
      majority = max(window.count(c) for c in set(window))
      if len(window) - majority <= k:
        best = max(best, len(window))
  return best


class TestCharacterReplacement(unittest.TestCase):
  def test_example_abab(self):
    self.assertEqual(character_replacement("ABAB", 2), 4)

  def test_example_aababba(self):
    self.assertEqual(character_replacement("AABABBA", 1), 4)

  def test_no_changes_allowed(self):
    self.assertEqual(character_replacement("ABCDE", 0), 1)

  def test_already_uniform(self):
    self.assertEqual(character_replacement("AAAA", 0), 4)

  def test_single_character(self):
    self.assertEqual(character_replacement("A", 5), 1)

  def test_budget_larger_than_string(self):
    self.assertEqual(character_replacement("ABCD", 10), 4)

  def test_run_at_the_end(self):
    self.assertEqual(character_replacement("BAAAB", 1), 4)

  def test_matches_brute_force(self):
    cases = ["AABBBCC", "ABBABBA", "CCCCA", "ABABABAB", "XYZXYZ", "AAABBB"]
    for s in cases:
      for k in range(0, 4):
        self.assertEqual(character_replacement(s, k), brute_force(s, k),
                         "s=%s k=%d" % (s, k))


if __name__ == '__main__':
  unittest.main()
