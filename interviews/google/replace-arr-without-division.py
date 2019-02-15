# https://www.glassdoor.com/Interview/google-software-engineer-interview-questions-SRCH_KE0,24.htm
# Given an array of numbers, replace each number with the product of all
# the numbers in the array except the number itself *without* using division.

import unittest


def arr_prod(arr):
  n = len(arr)

  if n <= 1:
    return list(arr)

  products = [[0, 0] for i in range(n)]
  product_i = 1
  product_j = 1

  for i in range(n):
    j = n - i - 1
    product_i *= arr[i]
    product_j *= arr[j]
    products[i][0] = product_i
    products[j][1] = product_j

  out = [0] * n
  for i in range(n):
    if i == 0:
      out[i] = products[i+1][1]
    elif i == n - 1:
      out[i] = products[i-1][0]
    else:
      out[i] = products[i-1][0] * products[i+1][1]

  return out


class TestArrProduct(unittest.TestCase):
  def test_ok(self):
    res = arr_prod([-2, 12, 3, -6, 21])
    self.assertTrue(res[0] == (12 * 3 * -6 * 21))
    self.assertTrue(res[1] == (-2 * 3 * -6 * 21))
    self.assertTrue(res[4] == (-2 * 12 * 3 * -6))

  def test_weird_size(self):
    res = arr_prod([2])
    self.assertTrue(res[0] == 2)

    res = arr_prod([])
    self.assertTrue(res == [])


if __name__ == '__main__':
  unittest.main()
