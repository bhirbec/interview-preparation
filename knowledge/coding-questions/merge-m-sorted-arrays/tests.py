import unittest


class TestMergeSortedArrays(unittest.TestCase):
  def test_no_arrays(self):
    self.assertEqual(merge_sorted_arrays([]), [])

  def test_single_array(self):
    self.assertEqual(merge_sorted_arrays([[1, 2, 3]]), [1, 2, 3])

  def test_all_arrays_empty(self):
    self.assertEqual(merge_sorted_arrays([[], [], []]), [])

  def test_some_arrays_empty(self):
    self.assertEqual(merge_sorted_arrays([[], [2], []]), [2])

  def test_equal_length_arrays(self):
    arrays = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    self.assertEqual(merge_sorted_arrays(arrays), [1, 2, 3, 4, 5, 6, 7, 8, 9])

  def test_different_lengths(self):
    arrays = [[1, 4, 7], [2, 5], [3, 6, 8, 10]]
    self.assertEqual(merge_sorted_arrays(arrays), [1, 2, 3, 4, 5, 6, 7, 8, 10])

  def test_duplicates_across_arrays(self):
    arrays = [[1, 1, 45], [1, 4, 23], [5, 11, 22]]
    self.assertEqual(
      merge_sorted_arrays(arrays),
      [1, 1, 1, 4, 5, 11, 22, 23, 45],
    )

  def test_negative_numbers(self):
    arrays = [[-5, -1, 3], [-4, 0, 2], [-10, 7]]
    self.assertEqual(
      merge_sorted_arrays(arrays),
      [-10, -5, -4, -1, 0, 2, 3, 7],
    )

  def test_single_element_arrays(self):
    self.assertEqual(merge_sorted_arrays([[3], [1], [2]]), [1, 2, 3])


if __name__ == '__main__':
  unittest.main()
