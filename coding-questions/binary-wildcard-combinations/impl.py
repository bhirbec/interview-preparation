# Binary Wildcard Combinations
#
# Difficulty: easy
# Tags: #recursion #backtracking #string
# Source: https://www.careercup.com/question?id=20308668
#
# You are given a string `s` consisting only of the characters '0', '1', and
# '?'. Each '?' is a wildcard that can be either '0' or '1'. Return a list of
# all strings obtainable by replacing every '?' with '0' or '1'. Fixed '0'/'1'
# characters stay in place.
#
# If there are k wildcards, there are exactly 2^k results. Return them in
# ascending binary order: at each wildcard, try '0' before '1', scanning left
# to right (so the leftmost '?' is the most significant bit).
#
# Constraints:
#   - 0 <= len(s)
#   - every character is '0', '1', or '?'
#   - the number of '?' is small enough that 2^k results fit in memory
#
# Examples:
#   "1?"    -> ["10", "11"]
#   "?0?"   -> ["000", "001", "100", "101"]
#   "101"   -> ["101"]          (no wildcards: the string itself)
#   "?"     -> ["0", "1"]
#   ""      -> [""]             (one empty combination)
#
# Approach: backtracking. Walk the string; at a fixed character recurse to the
# next position; at a '?' set it to '0' then '1', recursing after each, and
# restore it to '?' on the way back. Record the string when the end is reached.

import unittest


def binary_wildcard_combinations(s):
  results = []
  chars = list(s)
  n = len(chars)

  def backtrack(pos):
    if pos == n:
      results.append(''.join(chars))
      return

    if chars[pos] == '?':
      for bit in ('0', '1'):
        chars[pos] = bit
        backtrack(pos + 1)
      chars[pos] = '?'
    else:
      backtrack(pos + 1)

  backtrack(0)
  return results


class TestBinaryWildcardCombinations(unittest.TestCase):
  def test_trailing_wildcard(self):
    self.assertEqual(binary_wildcard_combinations('1?'), ['10', '11'])

  def test_wildcard_between_fixed(self):
    self.assertEqual(
        binary_wildcard_combinations('?0?'),
        ['000', '001', '100', '101'],
    )

  def test_no_wildcard_returns_itself(self):
    self.assertEqual(binary_wildcard_combinations('101'), ['101'])

  def test_single_wildcard(self):
    self.assertEqual(binary_wildcard_combinations('?'), ['0', '1'])

  def test_empty_string(self):
    self.assertEqual(binary_wildcard_combinations(''), [''])

  def test_two_wildcards_ascending_order(self):
    self.assertEqual(
        binary_wildcard_combinations('??'),
        ['00', '01', '10', '11'],
    )

  def test_three_wildcards_full_binary_count(self):
    self.assertEqual(
        binary_wildcard_combinations('???'),
        ['000', '001', '010', '011', '100', '101', '110', '111'],
    )

  def test_all_fixed_no_expansion(self):
    self.assertEqual(binary_wildcard_combinations('0010'), ['0010'])

  def test_count_is_two_to_the_k(self):
    s = '10??1??01???'
    out = binary_wildcard_combinations(s)
    self.assertEqual(len(out), 2 ** s.count('?'))
    self.assertEqual(len(set(out)), len(out))  # all distinct

  def test_fixed_positions_are_preserved(self):
    out = binary_wildcard_combinations('1?0?')
    for combo in out:
      self.assertEqual(combo[0], '1')
      self.assertEqual(combo[2], '0')


if __name__ == '__main__':
  unittest.main()
