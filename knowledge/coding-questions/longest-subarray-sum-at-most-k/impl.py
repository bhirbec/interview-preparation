# Longest Subarray With Sum At Most K
#
# Difficulty: medium
# Tags: #array #two-pointers #sharethis
#
# You are given an array of positive integers `a` and a non-negative integer
# `k`. Consider all contiguous subarrays of `a` whose elements sum to at most
# `k`. Return the length of the longest such subarray, or 0 if no subarray
# qualifies (which happens only when every single element already exceeds `k`).
#
# Constraints:
#   - 0 <= len(a)
#   - a[i] >= 1 for every element (all values are positive)
#   - 0 <= k
#
# Examples:
#   a = [3, 1, 2, 3, 4], k = 3   -> 2   (subarray [1, 2] sums to 3)
#   a = [1, 1, 1, 1],    k = 2   -> 2   ([1, 1])
#   a = [5, 6, 7],       k = 4   -> 0   (every element already exceeds k)
#   a = [1, 2, 3],       k = 100 -> 3   (the whole array fits)
#   a = [2],             k = 2   -> 1   (single element exactly equal to k)
#   a = [],              k = 5   -> 0   (empty array)
#
# Approach: sliding window. Grow the window by advancing the right edge; whenever
# the running sum exceeds k, shrink from the left until it fits again. Because
# all values are positive, the window sum is monotonic, so each index enters and
# leaves the window at most once (O(n)). Track the largest valid window seen.


def longest_subarray_at_most_k(a, k):
  # TODO: implement
  raise NotImplementedError
