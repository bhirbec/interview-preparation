# Binary Wildcard Combinations
#
# Source: https://www.careercup.com/question?id=20308668
#
# You are given a string `s` consisting only of the characters '0', '1', and
# '?'. Each '?' is a wildcard that can be either '0' or '1'. Return a list of
# all strings obtainable by replacing every '?' with '0' or '1'. Fixed '0'/'1'
# characters stay in place.
#
# If there are k wildcards, there are exactly 2^k results. Return them in
# ascending binary order: at each wildcard, try '0' before '1', scanning left
# to right (so the leftmost '?' is the most significant bit).
#
# Constraints:
#   - 0 <= len(s)
#   - every character is '0', '1', or '?'
#   - the number of '?' is small enough that 2^k results fit in memory
#
# Examples:
#   "1?"    -> ["10", "11"]
#   "?0?"   -> ["000", "001", "100", "101"]
#   "101"   -> ["101"]          (no wildcards: the string itself)
#   "?"     -> ["0", "1"]
#   ""      -> [""]             (one empty combination)


def binary_wildcard_combinations(s):
  # TODO: implement
  raise NotImplementedError
