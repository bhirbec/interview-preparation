# Median Of Two Sorted Arrays Of Equal Size
#
# Difficulty: hard
# Tags: #array #binary-search
#
# You are given two arrays `a` and `b`, each sorted in non-decreasing order and
# each of the same length n. Conceptually merge them into a single sorted array
# of 2n elements and return its median. Because the merged length 2n is even,
# the median is defined here as the upper of the two middle elements, i.e. the
# element at index n (0-based) of the merged array. The overall run time should
# be O(log n).
#
# Constraints:
#   - len(a) == len(b) == n, with n >= 1
#   - a and b are each sorted in non-decreasing order
#
# Examples:
#   a = [1, 2, 3, 4], b = [5, 6, 7, 8]  -> 5
#       (merged [1,2,3,4,5,6,7,8], index 4 is 5)
#   a = [1, 3, 5],    b = [2, 4, 6]     -> 4
#       (merged [1,2,3,4,5,6], index 3 is 4)
#   a = [5],          b = [9]           -> 9   (merged [5,9], index 1)
#   a = [1,12,15,26,38], b = [2,13,17,30,45] -> 17
#       (merged index 5; the two middles are 15 and 17, upper is 17)
#
# Approach: divide and conquer. Compare the medians of the two current windows.
# The overall median cannot lie in the lower half of the array with the smaller
# median nor in the upper half of the array with the larger median, so discard
# those halves and recurse on windows half the size each round -> O(log n).


def find_median(a, b):
  # TODO: implement
  raise NotImplementedError
