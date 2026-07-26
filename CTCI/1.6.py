# String Compression
#
# Difficulty: easy
# Tags: #string
#
# You are given a string. Return a run-length encoding of it: each maximal run
# of a repeated character `c` of length `k` is written as `c` followed by `k`.
# Every run is emitted, including runs of length 1.
#
# Constraints:
#   - 0 <= len(s)
#   - s may contain any characters; runs are compared by exact character
#
# Examples:
#   "aaaannnnfffgggnngg" -> "a4n4f3g3n2g2"
#   "aabcccccaaa"        -> "a2b1c5a3"
#   "abc"                -> "a1b1c1"   (runs of length 1 still get a count)
#   "a"                  -> "a1"
#   ""                   -> ""
#
# Note: the canonical CTCI variant returns the original string when the encoded
# form would not be shorter (e.g. "abc" -> "abc"); this port always returns the
# encoded form, matching the original Go implementation.
#
# Approach: walk the string tracking the current character and its run length;
# when the character changes, flush "<char><count>" and reset the count.

import unittest


def compress(s):
  if not s:
    return ''

  count = 1
  prev_char = s[0]
  buf = []

  for char in s[1:]:
    if char == prev_char:
      count += 1
    else:
      buf.append(prev_char)
      buf.append(str(count))
      count = 1
    prev_char = char

  buf.append(prev_char)
  buf.append(str(count))

  return ''.join(buf)


class TestCompress(unittest.TestCase):
  def test_go_source_example(self):
    self.assertEqual(compress('aaaannnnfffgggnngg'), 'a4n4f3g3n2g2')

  def test_ctci_example(self):
    self.assertEqual(compress('aabcccccaaa'), 'a2b1c5a3')

  def test_all_distinct_still_counted(self):
    self.assertEqual(compress('abc'), 'a1b1c1')

  def test_single_character(self):
    self.assertEqual(compress('a'), 'a1')

  def test_empty_string(self):
    self.assertEqual(compress(''), '')

  def test_single_long_run(self):
    self.assertEqual(compress('aaaa'), 'a4')

  def test_case_sensitive(self):
    self.assertEqual(compress('aAaA'), 'a1A1a1A1')

  def test_run_of_ten(self):
    self.assertEqual(compress('aaaaaaaaaa'), 'a10')


if __name__ == '__main__':
  unittest.main()
