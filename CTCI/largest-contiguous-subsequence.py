# Contiguous Sequence
# Difficulty: medium
# Tags: #array #dynamic-programming #subsequence
#
# You are given an array of integers (positive and negative). Find the
# contiguous subarray with the largest sum and return that sum together with the
# start and end indices of the subarray, as a tuple (max_sum, start, end).
#
# If every element is negative (or the array is empty), the largest achievable
# sum is 0 (choosing the empty subarray), and (0, 0, 0) is returned.
#
# Examples:
#   [-1, 2, 3, -3, 2, 3, 4, -4] -> (11, 1, 6)  (subarray [2, 3, -3, 2, 3, 4])
#   [-2, 1, -3, 4, -1, 2, 1, -5, 4] -> (6, 3, 6)  (subarray [4, -1, 2, 1])
#   [5]                          -> (5, 0, 0)
#   [-1, -2, -3]                 -> max sum 0  (all negative -> empty subarray;
#                                                the reported indices are unused)
#
# Approach: Kadane's algorithm. Sweep the array keeping a running sum; reset it
# to 0 (and advance the candidate start index) whenever it drops below 0, and
# record a new maximum with its end index whenever the running sum exceeds the
# best seen so far.

import unittest


def largest(array):
  current_sum = 0
  max_sum = 0
  start, end = 0, 0

  for k, value in enumerate(array):
    current_sum += value
    if current_sum < 0:
      current_sum = 0
      start = k + 1
    elif current_sum > max_sum:
      max_sum = current_sum
      end = k

  return max_sum, start, end


class TestLargest(unittest.TestCase):
  def test_canonical_example(self):
    self.assertEqual(largest([-1, 2, 3, -3, 2, 3, 4, -4]), (11, 1, 6))

  def test_kadane_example(self):
    self.assertEqual(largest([-2, 1, -3, 4, -1, 2, 1, -5, 4]), (6, 3, 6))

  def test_single_positive(self):
    self.assertEqual(largest([5]), (5, 0, 0))

  def test_all_negative_returns_zero(self):
    # No non-empty subarray beats the empty one, so the max sum is 0.
    # (The returned indices are meaningless in this case and not asserted.)
    self.assertEqual(largest([-1, -2, -3])[0], 0)

  def test_empty_array(self):
    self.assertEqual(largest([]), (0, 0, 0))

  def test_all_positive(self):
    self.assertEqual(largest([1, 2, 3, 4]), (10, 0, 3))

  def test_leading_negative(self):
    self.assertEqual(largest([-5, 4]), (4, 1, 1))


if __name__ == '__main__':
  unittest.main()
