# Restore Set From Pair Sums
# Source: https://www.careercup.com/question?id=5751343965798400
#
# There was a collection X of N numbers (N >= 3, duplicates allowed). Someone
# computed the sum of every unordered pair — all N * (N - 1) / 2 of them — and
# handed you those pair sums in arbitrary order. The original collection is
# lost.
#
# Reconstruct it: return a list of N numbers whose multiset of pairwise sums
# is exactly the input. More than one collection can produce the same sums
# (some reconstructions may involve non-integer values even when the sums are
# integers) — ANY valid answer is accepted, in any order.
#
# Constraints:
#   - the input is a valid multiset of pair sums for some collection, N >= 3
#
# Examples:
#   restore_set([3, 4, 5])             -> [1, 2, 3]
#   restore_set([3, 4, 5, 18, 19, 20]) -> [1, 2, 3, 17]
#     # ...but [-5.5, 8.5, 9.5, 10.5] has the same pair sums and is accepted too
#   restore_set([10, 10, 10])          -> [5, 5, 5]


def restore_set(sums):
  # TODO: implement
  raise NotImplementedError
