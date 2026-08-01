import unittest


class TestFindPeakElement(unittest.TestCase):
  def assert_is_peak(self, nums, index):
    self.assertIsInstance(index, int)
    self.assertTrue(0 <= index < len(nums),
                    "index %r out of range for %r" % (index, nums))
    if index > 0:
      self.assertGreater(nums[index], nums[index - 1], str(nums))
    if index < len(nums) - 1:
      self.assertGreater(nums[index], nums[index + 1], str(nums))

  def test_example(self):
    self.assertEqual(find_peak_element([1, 2, 3, 1]), 2)

  def test_several_peaks(self):
    nums = [1, 2, 1, 3, 5, 6, 4]
    self.assert_is_peak(nums, find_peak_element(nums))

  def test_single_element(self):
    self.assertEqual(find_peak_element([1]), 0)

  def test_strictly_decreasing(self):
    self.assertEqual(find_peak_element([3, 2, 1]), 0)

  def test_strictly_increasing(self):
    self.assertEqual(find_peak_element([1, 2, 3, 4]), 3)

  def test_two_elements(self):
    self.assertEqual(find_peak_element([1, 2]), 1)
    self.assertEqual(find_peak_element([2, 1]), 0)

  def test_negative_values(self):
    nums = [-5, -2, -9, -1]
    self.assert_is_peak(nums, find_peak_element(nums))

  def test_zigzag(self):
    nums = [1, 5, 2, 6, 3, 7, 4]
    self.assert_is_peak(nums, find_peak_element(nums))

  def test_every_sawtooth_shape(self):
    cases = [
        [10, 20, 15, 2, 23, 90, 67],
        [6, 5, 4, 3, 2, 3, 2],
        [1, 3, 2, 4, 1, 5, 0],
        [0, 1],
    ]
    for nums in cases:
      self.assert_is_peak(nums, find_peak_element(nums))


if __name__ == '__main__':
  unittest.main()
