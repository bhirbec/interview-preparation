# Make Array Consecutive
#
# Difficulty: easy
# Tags: #array #math
#
# You are given an array of distinct non-negative integers `statues`, where each
# value is the size of a statue you own. You want your collection to contain
# every size in a consecutive range with no gaps — that is, for the smallest and
# largest sizes you end up with, you must own a statue of every integer size in
# between.
#
# Return the minimum number of additional statues you need to acquire so that the
# sizes you own form such a gap-free consecutive range.
#
# Constraints:
#   - 1 <= len(statues) <= 1000
#   - 0 <= statues[i] <= 20000
#   - all values in statues are distinct
#
# Examples:
#   [6, 2, 3, 8]  -> 3   (needs 4, 5, 7 to fill 2..8)
#   [0, 3]        -> 2   (needs 1, 2)
#   [5, 4, 6]     -> 0   (already consecutive)
#   [6]           -> 0   (a single statue is trivially consecutive)
#
# Approach: answer = (max - min + 1) - len(statues), using exact integer math.


def make_array_consecutive(statues):
  # TODO: implement
  raise NotImplementedError
