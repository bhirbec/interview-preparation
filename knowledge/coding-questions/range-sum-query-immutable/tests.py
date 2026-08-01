import unittest


class TestNumArray(unittest.TestCase):
  def setUp(self):
    self.array = NumArray([-2, 0, 3, -5, 2, -1])

  def test_example_prefix(self):
    self.assertEqual(self.array.sum_range(0, 2), 1)

  def test_example_suffix(self):
    self.assertEqual(self.array.sum_range(2, 5), -1)

  def test_whole_range(self):
    self.assertEqual(self.array.sum_range(0, 5), -3)

  def test_single_element(self):
    self.assertEqual(self.array.sum_range(3, 3), -5)

  def test_repeated_queries_are_stable(self):
    for _ in range(3):
      self.assertEqual(self.array.sum_range(1, 4), 0)

  def test_single_element_array(self):
    self.assertEqual(NumArray([7]).sum_range(0, 0), 7)

  def test_all_zeros(self):
    self.assertEqual(NumArray([0, 0, 0]).sum_range(0, 2), 0)

  def test_every_subrange(self):
    nums = [4, -1, 2, 0, 6]
    array = NumArray(nums)
    for left in range(len(nums)):
      for right in range(left, len(nums)):
        self.assertEqual(array.sum_range(left, right),
                         sum(nums[left:right + 1]),
                         "range %d..%d" % (left, right))


if __name__ == '__main__':
  unittest.main()
