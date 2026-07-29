import unittest
from math import factorial


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
