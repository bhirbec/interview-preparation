# Check Permutation
# Difficulty: easy
# Tags: #string #hashtable #sorting
#
# You are given two strings, s1 and s2. Return True if one is a permutation of
# the other (same characters with the same counts, in any order), and False
# otherwise.
#
# The comparison is case-sensitive and counts every character, including spaces.
# Two strings of different lengths can never be permutations of each other.
#
# Examples:
#   ("abc", "cba")   -> True   (same characters reordered)
#   ("abc", "abd")   -> False  (different characters)
#   ("abc", "ab")    -> False  (different lengths)
#   ("", "")         -> True   (two empty strings)
#   ("aab", "abb")   -> False  (counts differ)
#
# Approach: is_permutation_naive sorts both strings and compares them
# (O(n log n)). is_permutation counts characters of s1 in a hash map, then
# decrements those counts while scanning s2; every count must end at zero (O(n)).

import unittest


def is_permutation_naive(s1, s2):
  '''
  Return True if s1 is a permutation of s2. Otherwise return False.
  Running Time O(nlogn)
  Space O(n)
  '''
  if len(s1) != len(s2):
    return False

  return sorted(s1) == sorted(s2)


def is_permutation(s1, s2):
  '''
  Return True if s1 is a permutation of s2. Otherwise return False.
  Running Time O(n)
  Space O(n)
  '''
  if len(s1) != len(s2):
    return False

  chars = {}
  for c in s1:
    chars[c] = chars.setdefault(c, 0) + 1

  for c in s2:
    if c not in chars:
      return False
    chars[c] -= 1

  return all(v == 0 for v in list(chars.values()))


class TestPerm(unittest.TestCase):

  def test_is_permutation_length(self):
    self.assertFalse(is_permutation('sew', 's'))

  def test_is_permutation_small(self):
    self.assertTrue(is_permutation('sew', 'wse'))

  def test_is_permutation_big(self):
    self.assertTrue(is_permutation('sewJdifjldifjdkwdkdsk', 'skeJdjwdkkdsilwjdiffd'))

  def test_is_permutation_notok(self):
    self.assertFalse(is_permutation('sew', 'wwse'))

  def test_is_permutation_empty(self):
    self.assertTrue(is_permutation('', ''))

  def test_is_permutation_case_sensitive(self):
    self.assertFalse(is_permutation('abc', 'abC'))

  def test_is_permutation_same_length_diff_chars(self):
    self.assertFalse(is_permutation('abc', 'abd'))

  def test_is_permutation_counts_differ(self):
    self.assertFalse(is_permutation('aab', 'abb'))


class TestPermNaive(unittest.TestCase):

  def test_is_permutation_naive_length(self):
    self.assertFalse(is_permutation_naive('sew', 's'))

  def test_is_permutation_naive_true(self):
    self.assertTrue(is_permutation_naive('abc', 'cba'))

  def test_is_permutation_naive_false(self):
    self.assertFalse(is_permutation_naive('abc', 'abd'))

  def test_is_permutation_naive_empty(self):
    self.assertTrue(is_permutation_naive('', ''))


if __name__ == '__main__':
  unittest.main()
