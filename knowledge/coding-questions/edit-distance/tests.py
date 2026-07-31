import unittest


class TestEditDistance(unittest.TestCase):
  def test_classic_kitten(self):
    self.assertEqual(edit_distance('kitten', 'sitting'), 3)

  def test_classic_intention(self):
    self.assertEqual(edit_distance('intention', 'execution'), 5)

  def test_equal_strings(self):
    self.assertEqual(edit_distance('abc', 'abc'), 0)

  def test_both_empty(self):
    self.assertEqual(edit_distance('', ''), 0)

  def test_empty_to_string_is_all_inserts(self):
    self.assertEqual(edit_distance('', 'abc'), 3)

  def test_string_to_empty_is_all_deletes(self):
    self.assertEqual(edit_distance('abc', ''), 3)

  def test_single_replace(self):
    self.assertEqual(edit_distance('cat', 'car'), 1)

  def test_single_insert(self):
    self.assertEqual(edit_distance('abc', 'abcd'), 1)

  def test_symmetry(self):
    self.assertEqual(edit_distance('sunday', 'saturday'),
                     edit_distance('saturday', 'sunday'))

  def test_totally_different(self):
    self.assertEqual(edit_distance('abc', 'xyz'), 3)


if __name__ == '__main__':
  unittest.main()
