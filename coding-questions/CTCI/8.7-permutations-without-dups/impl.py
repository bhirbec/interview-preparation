# Permutations without Dups
# Difficulty: medium
# Tags: #recursion #backtracking
#
# Write a method to compute all permutations of a string whose characters are
# all unique.
#
# Input:  a string `chars` with no repeated characters.
# Output: a list containing every permutation of `chars` (order unspecified).
#         For a string of length n there are exactly n! permutations.
#
# Approach: keep a buffer of n slots. Placing character i, try every free slot,
# recurse to place the next character, then undo the placement (backtracking).
# When all characters are placed, emit the buffer as a string.
#
# Examples:
#   perms('')    -> ['']
#   perms('a')   -> ['a']
#   perms('ab')  -> ['ab', 'ba']
#   perms('abc') -> 6 permutations


def perms(chars):
  # TODO: implement
  raise NotImplementedError
