# Non-overlapping Intervals
#
# You are given a list of intervals, each a pair [start, end) with start < end.
# Return the minimum number of intervals you have to remove so that the ones
# left over do not overlap each other.
#
# Intervals that only touch at an endpoint — [1, 2] and [2, 3] — do NOT overlap.
#
# Constraints:
#   - 0 <= len(intervals) <= 10^5
#   - start < end for every interval
#   - the input is in no particular order
#
# Examples:
#   [[1, 2], [2, 3], [3, 4], [1, 3]]  -> 1   (drop [1, 3])
#   [[1, 2], [1, 2], [1, 2]]          -> 2   (keep one copy)
#   [[1, 2], [2, 3]]                  -> 0   (touching is fine)
#   []                                -> 0


def erase_overlap_intervals(intervals):
  # TODO: implement
  raise NotImplementedError
