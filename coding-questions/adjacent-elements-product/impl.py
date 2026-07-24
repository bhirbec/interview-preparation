# Adjacent Elements Product
#
# Difficulty: easy
# Tags: #array #implementation
#
# Given an array of integers, find the pair of adjacent elements that has the
# largest product and return that product.
#
# The array has at least 2 elements. Elements may be negative, so the largest
# product can come from two negatives (e.g. -6 * -1 = 6) rather than the two
# largest positives.
#
# Examples:
#   [3, 6, -2, -5, 7, 3]  -> 21   (7 * 3)
#   [5, 1, 2, 3, 1, 40]   -> 40    (1 * 40)
#   [-1, -2]              -> 2     (-1 * -2)
#   [9, 5, 10, 2, 24, -1, -48]  -> 50  (5 * 10)
#   [1, 0, 1, 0, 1000]   -> 0     (best adjacent pair still multiplies to 0)
#
# Approach: scan each adjacent pair once, tracking the running maximum product.

import unittest


def adjacent_elements_product(arr):
  max_product = None
  for i in range(1, len((arr))):
    product = arr[i-1] * arr[i]
    if max_product is None or product > max_product:
      max_product = product

  return max_product


class TestAdjacentElementsProduct(unittest.TestCase):
  def test_mixed_signs(self):
    self.assertEqual(adjacent_elements_product([3, 6, -2, -5, 7, 3]), 21)

  def test_all_positive(self):
    self.assertEqual(adjacent_elements_product([5, 1, 2, 3, 1, 40]), 40)

  def test_two_negatives(self):
    self.assertEqual(adjacent_elements_product([-1, -2]), 2)

  def test_negative_tail(self):
    self.assertEqual(adjacent_elements_product([9, 5, 10, 2, 24, -1, -48]), 50)

  def test_zeros(self):
    self.assertEqual(adjacent_elements_product([1, 0, 1, 0, 1000]), 0)

  def test_minimum_length(self):
    self.assertEqual(adjacent_elements_product([4, 7]), 28)

  def test_all_negative(self):
    self.assertEqual(adjacent_elements_product([-6, -1, -3, -4]), 12)

  def test_best_is_first_pair(self):
    self.assertEqual(adjacent_elements_product([100, 100, 1, 2]), 10000)


if __name__ == '__main__':
  unittest.main()
