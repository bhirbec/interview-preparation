# Sparse Search
#
# You are given a sorted array of strings interspersed with empty strings
# (`''`), and a target non-empty string `value`. Return an index at which
# `value` occurs, or None if it is not present.
#
# Input:  a sorted list of strings (some of which may be ''), and a target.
# Output: an index i with arr[i] == value, or None if absent.
#
# The empty strings break a plain binary search because you cannot compare
# against them. Approach: probe within [start, end]; if the probe lands on an
# empty string, retry after trimming empty ends; otherwise recurse into the
# left or right half by comparing against the probe. (This implementation
# picks the probe index at random, which stays correct because empty ends are
# trimmed each step, guaranteeing progress.)
#
# Examples:
#   arr = ['at', '', '', '', 'ball', '', '', 'car', '', '', 'dad', '', '']
#   binary_search(arr, 'ball') -> 4
#   binary_search(arr, 'xxx')  -> None
#   binary_search([], 'xxx')   -> None


def binary_search(arr, value):
  # TODO: implement
  raise NotImplementedError
