# Check Palindrome
#
# Difficulty: easy
# Tags: #string #two-pointers
#
# Given the string, check if it is a palindrome — i.e. it reads the same left
# to right and right to left. Return True if it is a palindrome, otherwise
# return False. Comparison is character-for-character over the whole string
# (no case-folding or whitespace stripping); the input is a plain string that
# may be empty.
#
# Examples:
#   "aabaa"  -> True   (reversed is "aabaa")
#   "abac"   -> False  (reversed is "caba")
#   "a"      -> True   (single character)
#   ""       -> True   (empty string is trivially a palindrome)
#   "xx"     -> True   (reversed is "xx")
#
# Approach: walk two pointers inward from both ends, comparing characters;
# mismatch means not a palindrome. This is O(n) time and O(1) extra space.


def check_palindrome(input_string):
  # TODO: implement
  raise NotImplementedError
