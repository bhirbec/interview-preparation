# Power Set
# Difficulty: medium
# Tags: #recursion #backtracking
#
# Return all subsets of a set (the power set). The input is given as a sequence
# of distinct elements (here, the characters of a string), and each subset is
# returned as a string preserving the original order of the elements.
#
# Input: s, a string of distinct characters.
# Output: a list of strings, one per subset, including the empty subset ''. A
# set of n elements has 2**n subsets.
#
# Examples:
#   ''    -> ['']
#   'a'   -> ['', 'a']
#   'ab'  -> ['', 'a', 'ab', 'b']
#   'abc' -> ['', 'a', 'ab', 'abc', 'ac', 'b', 'bc', 'c']
#
# Approach: recursive enumeration. At each step append the current partial
# subset to the result, then extend it with each remaining element in turn
# (choosing elements only from positions after the current one avoids duplicates).


def subsets(s):
  # TODO: implement
  raise NotImplementedError
