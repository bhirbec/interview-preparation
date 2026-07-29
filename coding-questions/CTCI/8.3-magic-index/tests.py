import unittest


class TestMagicIndex(unittest.TestCase):
  def test_magic_in_middle(self):
    self.assertEqual(magic_index_distinct_array([-4, -2, 2, 3, 10]), 2)

  def test_no_magic_realistic(self):
    self.assertEqual(magic_index_distinct_array([-1, 0, 3, 5, 7]), -1)

  def test_magic_early(self):
    self.assertEqual(magic_index_distinct_array([-1, 1, 3, 5, 7]), 1)

  def test_no_magic_all_greater(self):
    self.assertEqual(magic_index_distinct_array([1, 2, 3, 4, 5]), -1)

  def test_no_magic_all_smaller(self):
    self.assertEqual(magic_index_distinct_array([-5, -4, -3, -2, -1]), -1)

  def test_magic_at_zero(self):
    self.assertEqual(magic_index_distinct_array([0, 2, 4, 6]), 0)

  def test_magic_at_last_index(self):
    self.assertEqual(magic_index_distinct_array([-2, -1, 0, 3]), 3)

  def test_empty_array(self):
    self.assertEqual(magic_index_distinct_array([]), -1)

  def test_single_element_magic(self):
    self.assertEqual(magic_index_distinct_array([0]), 0)

  def test_single_element_no_magic(self):
    self.assertEqual(magic_index_distinct_array([5]), -1)


if __name__ == '__main__':
  unittest.main()
