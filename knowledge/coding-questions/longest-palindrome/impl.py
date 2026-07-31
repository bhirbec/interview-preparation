# Longest Palindrome
#
# Difficulty: easy
# Source: https://www.careercup.com/question?id=5631060781039616
# Tags: #string #hashtable #google
#
# You are given a string `s`. By removing and rearranging its characters, build
# the longest palindrome possible and return it. If several palindromes share the
# maximum length, returning any one of them is acceptable.
#
# Constraints:
#   - 0 <= len(s)
#   - characters may repeat
#
# Examples:
#   "aha"                   -> "aha"           (length 3)
#   "abc"                   -> "a"             (any single character)
#   "gggaaa"                -> "agaga"         (length 5; one leftover unused)
#   "aabb"                  -> "abba"          (length 4, no center char)
#   ""                      -> ""
#
# Approach: count each character; use floor(count/2) pairs on each side, and place
# one leftover odd character in the middle if any character has an odd count.


def longest_palindrome(s):
  # TODO: implement
  raise NotImplementedError
