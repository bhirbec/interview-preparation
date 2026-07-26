# Permutations without Dups
# Difficulty: medium
# Tags: #recursion #backtracking
#
# Write a method to compute all permutations of a string whose characters are
# all unique.
#
# Input:  a string `chars` with no repeated characters.
# Output: a list containing every permutation of `chars` (order unspecified).
#         For a string of length n there are exactly n! permutations.
#
# Approach: keep a buffer of n slots. Placing character i, try every free slot,
# recurse to place the next character, then undo the placement (backtracking).
# When all characters are placed, emit the buffer as a string.
#
# Examples:
#   perms('')    -> ['']
#   perms('a')   -> ['a']
#   perms('ab')  -> ['ab', 'ba']
#   perms('abc') -> 6 permutations

import unittest
from math import factorial


def perms(chars):
  n = len(chars)
  buff = [''] * n

  def _f(i):
    if i == n:
      yield ''.join(buff)
      return

    for j in range(n):
      if buff[j] == '':
        buff[j] = chars[i]
        for p in _f(i + 1):
          yield p
        buff[j] = ''

  return list(_f(0))


class TestPermutationsWithoutDups(unittest.TestCase):
  def test_empty_string(self):
    self.assertEqual(perms(''), [''])

  def test_single_char(self):
    self.assertEqual(perms('a'), ['a'])

  def test_two_chars(self):
    self.assertEqual(sorted(perms('ab')), ['ab', 'ba'])

  def test_three_chars_full_enumeration(self):
    self.assertEqual(
      sorted(perms('abc')),
      ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'],
    )

  def test_count_is_factorial(self):
    for s in ['a', 'ab', 'abc', 'abcd', 'abcde']:
      self.assertEqual(len(perms(s)), factorial(len(s)))

  def test_all_permutations_distinct_and_valid(self):
    s = 'abcd'
    result = perms(s)
    self.assertEqual(len(result), len(set(result)))
    for p in result:
      self.assertEqual(sorted(p), sorted(s))


if __name__ == '__main__':
  unittest.main()
