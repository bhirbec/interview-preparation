# Count Palindromic Substrings
#
# Difficulty: medium
# Tags: #string #two-pointers #sharethis
#
# You are given a string `s`. Return the number of non-empty contiguous
# substrings of `s` that are palindromes. Substrings that occupy different
# positions are counted separately even if they are identical in text, and every
# single character counts as a palindrome of length 1.
#
# Constraints:
#   - 0 <= len(s)
#   - s consists of arbitrary characters (comparison is exact/case-sensitive)
#
# Examples:
#   "abc"    -> 3   ("a", "b", "c")
#   "aaa"    -> 6   ("a"x3, "aa"x2, "aaa")
#   "aba"    -> 4   ("a", "b", "a", "aba")
#   "abccba" -> 9   (6 singles + "cc" + "bccb" + "abccba")
#   ""       -> 0
#   "a"      -> 1
#
# Approach: expand around each center. There are 2*n - 1 possible centers (each
# character and each gap between two characters). From each center, expand
# outward while the two ends match, counting one palindrome per successful
# expansion. Runs in O(n^2) time and O(1) space.


def count_palindromic_substrings(s):
  # TODO: implement
  raise NotImplementedError
