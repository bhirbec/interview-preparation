# Count ABC Strings
#
# Difficulty: medium
# Source: https://www.careercup.com/question?id=5717453712654336
# Tags: #dynamic-programming #recursion #google
#
# Given a length n, return how many strings of length n can be formed from the
# letters 'a', 'b' and 'c' subject to two rules:
#   - the string contains at most one 'b', and
#   - it never contains three or more consecutive 'c' (at most two in a row).
#
# Constraints:
#   - n >= 0. The empty string (n = 0) counts as 1 valid string.
#
# Examples:
#   n = 1 -> 3     # a, b, c
#   n = 2 -> 8     # all 9 pairs except "bb"
#   n = 3 -> 19    # e.g. aaa, aab, aba, abc, cca, ccb, ... (excludes bb*, ccc)
#   n = 4 -> 43
#
# Approach: count with a memoized recursion over (position, number of 'b' used,
# current run of consecutive 'c'), branching on placing 'a', 'b' or 'c'.


def count_abc_strings(n):
  # TODO: implement
  raise NotImplementedError
