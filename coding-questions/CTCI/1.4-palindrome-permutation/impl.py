# Palindrome Permutation
# Difficulty: easy
# Tags: #string #hashtable
#
# You are given a string s. Return True if any permutation of s is a palindrome,
# and False otherwise. A permutation is a rearrangement of the characters.
#
# The check is case-insensitive and ignores spaces. A string can be rearranged
# into a palindrome exactly when at most one distinct character has an odd count
# (that single odd-count character can sit in the middle).
#
# Examples:
#   "Tact Coa" -> True   (permutation "taco cat" / "atco cta" is a palindrome)
#   "aab"      -> True   (permutation "aba")
#   "abc"      -> False  (three characters each appear an odd number of times)
#   ""         -> True   (empty string is a palindrome)
#
# Approach: count occurrences of each character (after lowercasing and dropping
# spaces), then verify that no more than one character has an odd count.


def check_perm_of_palindrome(s):
  # TODO: implement
  raise NotImplementedError
