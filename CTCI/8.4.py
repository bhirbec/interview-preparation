# Power Set
# Difficulty: medium
# Tags: #recursion #backtracking
#
# Return all subsets of a set (the power set). The input is given as a sequence
# of distinct elements (here, the characters of a string), and each subset is
# returned as a string preserving the original order of the elements.
#
# Input: s, a string of distinct characters.
# Output: a list of strings, one per subset, including the empty subset ''. A
# set of n elements has 2**n subsets.
#
# Examples:
#   ''    -> ['']
#   'a'   -> ['', 'a']
#   'ab'  -> ['', 'a', 'ab', 'b']
#   'abc' -> ['', 'a', 'ab', 'abc', 'ac', 'b', 'bc', 'c']
#
# Approach: recursive enumeration. At each step append the current partial
# subset to the result, then extend it with each remaining element in turn
# (choosing elements only from positions after the current one avoids duplicates).

import unittest


def subsets(s):
  n = len(s)
  buf = [''] * n
  result = []

  def _f(i, d):
    if d > n:
      return

    result.append(''.join(buf[:d]))

    for j in range(i, n):
      buf[d] = s[j]
      _f(j + 1, d + 1)

  _f(0, 0)
  return result


class TestPowerSet(unittest.TestCase):
  def test_empty_string(self):
    self.assertEqual(subsets(''), [''])

  def test_single_element(self):
    self.assertEqual(sorted(subsets('a')), ['', 'a'])

  def test_two_elements(self):
    self.assertEqual(sorted(subsets('ab')), sorted(['', 'a', 'ab', 'b']))

  def test_three_elements(self):
    expected = ['', 'a', 'ab', 'abc', 'ac', 'b', 'bc', 'c']
    self.assertEqual(sorted(subsets('abc')), sorted(expected))

  def test_count_is_power_of_two(self):
    for s in ['', 'a', 'ab', 'abcd', 'abcde']:
      self.assertEqual(len(subsets(s)), 2 ** len(s))

  def test_all_subsets_unique(self):
    result = subsets('abcd')
    self.assertEqual(len(result), len(set(result)))

  def test_empty_subset_included(self):
    self.assertIn('', subsets('xyz'))

  def test_full_set_included(self):
    self.assertIn('abc', subsets('abc'))


if __name__ == '__main__':
  unittest.main()
