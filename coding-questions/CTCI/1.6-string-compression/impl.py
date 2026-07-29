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


def compress(s):
  # TODO: implement
  raise NotImplementedError
