import unittest


def _brute_force(s):
  n = len(s)
  total = 0
  for i in range(n):
    for j in range(i + 1, n + 1):
      sub = s[i:j]
      if sub == sub[::-1]:
        total += 1
  return total


class TestCountPalindromicSubstrings(unittest.TestCase):
  def test_all_distinct(self):
    self.assertEqual(count_palindromic_substrings("abc"), 3)

  def test_all_identical(self):
    self.assertEqual(count_palindromic_substrings("aaa"), 6)

  def test_odd_palindrome(self):
    self.assertEqual(count_palindromic_substrings("aba"), 4)

  def test_nested_even_palindrome(self):
    self.assertEqual(count_palindromic_substrings("abccba"), 9)

  def test_empty_string(self):
    self.assertEqual(count_palindromic_substrings(""), 0)

  def test_single_character(self):
    self.assertEqual(count_palindromic_substrings("a"), 1)

  def test_two_equal_characters(self):
    self.assertEqual(count_palindromic_substrings("aa"), 3)

  def test_two_different_characters(self):
    self.assertEqual(count_palindromic_substrings("ab"), 2)

  def test_case_sensitive(self):
    # "Aa" is not a palindrome under exact comparison.
    self.assertEqual(count_palindromic_substrings("Aa"), 2)

  def test_matches_brute_force(self):
    for s in ["", "a", "abba", "racecar", "aabaa", "xyzzyx", "abcba", "mississippi"]:
      self.assertEqual(count_palindromic_substrings(s), _brute_force(s), s)


if __name__ == '__main__':
  unittest.main()
