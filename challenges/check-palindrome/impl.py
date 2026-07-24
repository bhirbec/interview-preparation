# Check Palindrome
#
# Difficulty: easy
# Tags: #string #two-pointers
#
# Given the string, check if it is a palindrome — i.e. it reads the same left
# to right and right to left. Return True if it is a palindrome, otherwise
# return False. Comparison is character-for-character over the whole string
# (no case-folding or whitespace stripping); the input is a plain string that
# may be empty.
#
# Examples:
#   "aabaa"  -> True   (reversed is "aabaa")
#   "abac"   -> False  (reversed is "caba")
#   "a"      -> True   (single character)
#   ""       -> True   (empty string is trivially a palindrome)
#   "xx"     -> True   (reversed is "xx")
#
# Approach: walk two pointers inward from both ends, comparing characters;
# mismatch means not a palindrome. This is O(n) time and O(1) extra space.
import unittest


def check_palindrome(input_string):
  left, right = 0, len(input_string) - 1
  while left < right:
    if input_string[left] != input_string[right]:
      return False
    left += 1
    right -= 1
  return True


class TestCheckPalindrome(unittest.TestCase):
  def test_example_palindrome(self):
    self.assertTrue(check_palindrome("aabaa"))

  def test_example_not_palindrome(self):
    self.assertFalse(check_palindrome("abac"))

  def test_single_character(self):
    self.assertTrue(check_palindrome("a"))

  def test_empty_string(self):
    self.assertTrue(check_palindrome(""))

  def test_two_equal_characters(self):
    self.assertTrue(check_palindrome("xx"))

  def test_two_different_characters(self):
    self.assertFalse(check_palindrome("ab"))

  def test_even_length_palindrome(self):
    self.assertTrue(check_palindrome("abba"))

  def test_case_sensitive_not_palindrome(self):
    self.assertFalse(check_palindrome("Aa"))

  def test_longer_palindrome(self):
    self.assertTrue(check_palindrome("racecar"))

  def test_mismatch_at_ends(self):
    self.assertFalse(check_palindrome("abca"))


if __name__ == '__main__':
  unittest.main()
