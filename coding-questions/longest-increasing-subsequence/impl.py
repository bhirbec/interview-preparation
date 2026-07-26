# Longest Increasing Subsequence
#
# Difficulty: medium
# Tags: #dynamic-programming #subsequence #array
#
# You are given an integer array `nums`. Return the length of the longest
# strictly increasing subsequence.
#
# A subsequence is a sequence derived from the array by deleting zero or more
# elements without changing the order of the remaining elements. "Strictly
# increasing" means each element is greater than the one before it (equal
# values cannot both be used).
#
# Constraints:
#   - 0 <= len(nums) <= 2500
#   - -10^4 <= nums[i] <= 10^4
#
# Examples:
#   [10, 9, 2, 5, 3, 7, 101, 18] -> 4   (e.g. 2, 3, 7, 101 or 2, 5, 7, 101)
#   [3, 2, 6, 4, 5, 1]           -> 3   (2, 4, 5)
#   [0, 1, 0, 3, 2, 3]           -> 4   (0, 1, 2, 3)
#   [7, 7, 7, 7, 7]              -> 1   (equal values can't extend each other)
#   []                           -> 0
#
# Approach: O(n^2) dynamic programming. dp[i] = length of the longest strictly
# increasing subsequence ending at index i; dp[i] = 1 + max(dp[j]) over all
# j < i with nums[j] < nums[i], or 1 if none. The answer is max(dp).

import unittest


def length_of_lis(nums):
  if not nums:
    return 0

  n = len(nums)
  dp = [1] * n

  for i in range(1, n):
    for j in range(i):
      if nums[i] > nums[j] and dp[j] + 1 > dp[i]:
        dp[i] = dp[j] + 1

  return max(dp)


class TestLengthOfLis(unittest.TestCase):
  def test_leetcode_example(self):
    self.assertEqual(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)

  def test_readme_example(self):
    self.assertEqual(length_of_lis([3, 2, 6, 4, 5, 1]), 3)

  def test_with_repeats_between_runs(self):
    self.assertEqual(length_of_lis([0, 1, 0, 3, 2, 3]), 4)

  def test_all_equal_is_strict(self):
    self.assertEqual(length_of_lis([7, 7, 7, 7, 7]), 1)

  def test_empty(self):
    self.assertEqual(length_of_lis([]), 0)

  def test_single_element(self):
    self.assertEqual(length_of_lis([42]), 1)

  def test_two_increasing(self):
    self.assertEqual(length_of_lis([1, 2]), 2)

  def test_two_decreasing(self):
    self.assertEqual(length_of_lis([2, 1]), 1)

  def test_already_sorted(self):
    self.assertEqual(length_of_lis([1, 2, 3, 4, 5]), 5)

  def test_strictly_decreasing(self):
    self.assertEqual(length_of_lis([5, 4, 3, 2, 1]), 1)

  def test_negatives(self):
    self.assertEqual(length_of_lis([-8, -2, -3, -1]), 3)

  def test_duplicates_do_not_count(self):
    # 1, 2, 3, 4 is length 4; the duplicate 3 cannot extend a 3.
    self.assertEqual(length_of_lis([1, 3, 2, 3, 4]), 4)

  def test_best_run_at_end(self):
    self.assertEqual(length_of_lis([9, 8, 1, 2, 3, 4]), 4)


if __name__ == '__main__':
  unittest.main()
