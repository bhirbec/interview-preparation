# Palindrome Permutation
# Difficulty: easy
# Tags: #string #hashtable
#
# You are given a string s. Return True if any permutation of s is a palindrome,
# and False otherwise. A permutation is a rearrangement of the characters.
#
# The check is case-insensitive and ignores spaces. A string can be rearranged
# into a palindrome exactly when at most one distinct character has an odd count
# (that single odd-count character can sit in the middle).
#
# Examples:
#   "Tact Coa" -> True   (permutation "taco cat" / "atco cta" is a palindrome)
#   "aab"      -> True   (permutation "aba")
#   "abc"      -> False  (three characters each appear an odd number of times)
#   ""         -> True   (empty string is a palindrome)
#
# Approach: count occurrences of each character (after lowercasing and dropping
# spaces), then verify that no more than one character has an odd count.

import unittest


def check_perm_of_palindrome(s):
  s = s.lower().replace(' ', '')

  chars = {}
  for c in s:
    chars[c] = chars.setdefault(c, 0) + 1

  found_odd = False
  for counter in chars.values():
    if is_even(counter):
      continue

    if not found_odd:
      found_odd = True
    else:
      return False

  return True


def is_even(i):
  return (i & 1) == 0


class TestEven(unittest.TestCase):
  def test_is_even(self):
    self.assertTrue(is_even(-22))
    self.assertTrue(is_even(0))
    self.assertTrue(is_even(4))

  def test_is_odd(self):
    self.assertFalse(is_even(3))
    self.assertFalse(is_even(-19))


class TestPermOfPalindrome(unittest.TestCase):
  def test_ok(self):
    self.assertTrue(check_perm_of_palindrome('Tact Coa'))

  def test_empty_string(self):
    self.assertTrue(check_perm_of_palindrome(''))

  def test_single_char(self):
    self.assertTrue(check_perm_of_palindrome('a'))

  def test_even_counts(self):
    self.assertTrue(check_perm_of_palindrome('aabb'))

  def test_one_odd_count(self):
    self.assertTrue(check_perm_of_palindrome('aab'))

  def test_multiple_odd_counts(self):
    self.assertFalse(check_perm_of_palindrome('abc'))

  def test_case_insensitive(self):
    self.assertTrue(check_perm_of_palindrome('AaBb'))

  def test_spaces_ignored(self):
    self.assertTrue(check_perm_of_palindrome('a a'))


if __name__ == '__main__':
  unittest.main()
