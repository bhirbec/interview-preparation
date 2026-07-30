import unittest


def _is_palindrome(s):
  return s == s[::-1]


class TestLongestPalindrome(unittest.TestCase):
  def test_returns_palindrome(self):
    result = longest_palindrome("baazzxkkkuiuoioiikaab")
    self.assertTrue(_is_palindrome(result))

  def test_all_same_char(self):
    self.assertEqual(longest_palindrome("aaaa"), "aaaa")

  def test_no_repeats_length_one(self):
    result = longest_palindrome("abc")
    self.assertEqual(len(result), 1)
    self.assertTrue(_is_palindrome(result))

  def test_even_counts_no_center(self):
    self.assertEqual(longest_palindrome("aabb"), "abba")

  def test_odd_center(self):
    result = longest_palindrome("aha")
    self.assertTrue(_is_palindrome(result))
    self.assertEqual(len(result), 3)

  def test_length_matches_theoretical_max(self):
    # gggaaa: g=3, a=3, both odd -> max length is total - 1 = 5.
    result = longest_palindrome("gggaaa")
    self.assertEqual(len(result), 5)
    self.assertTrue(_is_palindrome(result))

  def test_empty(self):
    self.assertEqual(longest_palindrome(""), "")

  def test_single_char(self):
    self.assertEqual(longest_palindrome("z"), "z")


if __name__ == '__main__':
  unittest.main()
