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
# Approach: count the characters of s1 in a hash map, then decrement those
# counts while scanning s2; the strings are permutations iff the lengths match
# and every count ends at zero (O(n)).


def is_permutation(s1, s2):
  # TODO: implement
  raise NotImplementedError
