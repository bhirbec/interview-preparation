# All Longest Strings
#
# Difficulty: easy
# Tags: #array #string
#
# You are given an array of strings `input_array`. Return an array containing all
# of its longest strings — every string whose length equals the maximum string
# length in the array — keeping their original relative order.
#
# Constraints:
#   - 1 <= len(input_array) <= 10
#   - 1 <= len(input_array[i]) <= 10
#   - the array contains at least one string
#
# Examples:
#   ["aba", "aa", "ad", "vcd", "aba"]  -> ["aba", "vcd", "aba"]
#     (max length is 3; "aba", "vcd", "aba" all have length 3, in order)
#
#   ["abc", "eeee", "abcd", "dcd"]     -> ["eeee", "abcd"]
#     (max length is 4)
#
#   ["a", "abc", "cba"]                -> ["abc", "cba"]
#
#   ["enn", "b"]                       -> ["enn"]
#
# Approach: find the maximum length in one pass, then collect all strings that
# match it in a second pass, preserving order.

import unittest


def all_longest_strings(input_array):
  # TODO: implement
  raise NotImplementedError


class TestAllLongestStrings(unittest.TestCase):
  def test_example_one(self):
    self.assertEqual(
        all_longest_strings(["aba", "aa", "ad", "vcd", "aba"]),
        ["aba", "vcd", "aba"],
    )

  def test_example_two(self):
    self.assertEqual(
        all_longest_strings(["abc", "eeee", "abcd", "dcd"]),
        ["eeee", "abcd"],
    )

  def test_two_of_same_max(self):
    self.assertEqual(all_longest_strings(["a", "abc", "cba"]), ["abc", "cba"])

  def test_single_longest(self):
    self.assertEqual(all_longest_strings(["enn", "b"]), ["enn"])

  def test_single_element(self):
    self.assertEqual(all_longest_strings(["hello"]), ["hello"])

  def test_all_same_length(self):
    self.assertEqual(all_longest_strings(["ab", "cd", "ef"]), ["ab", "cd", "ef"])

  def test_order_preserved(self):
    self.assertEqual(
        all_longest_strings(["xx", "y", "zz", "w", "vv"]),
        ["xx", "zz", "vv"],
    )


if __name__ == '__main__':
  unittest.main()
