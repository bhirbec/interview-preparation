import unittest


class TestListy(unittest.TestCase):
  def test_element_at(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertEqual(l.element_at(0), 1)
    self.assertEqual(l.element_at(3), 17)
    self.assertEqual(l.element_at(5), 34)
    self.assertEqual(l.element_at(6), -1)
    self.assertEqual(l.element_at(11236), -1)

  def test_find_at_start(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertEqual(l.find(1), 0)

  def test_find_in_middle(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertEqual(l.find(6), 2)
    self.assertEqual(l.find(17), 3)

  def test_find_at_end(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertEqual(l.find(34), 5)

  def test_find_absent_below_range(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertIsNone(l.find(0))

  def test_find_absent_within_range(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertIsNone(l.find(2))
    self.assertIsNone(l.find(35))

  def test_find_absent_above_range(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertIsNone(l.find(37))

  def test_find_empty(self):
    l = Listy([])
    self.assertIsNone(l.find(6))

  def test_find_single_element(self):
    self.assertEqual(Listy([5]).find(5), 0)
    self.assertIsNone(Listy([5]).find(9))
    self.assertIsNone(Listy([5]).find(1))

  def test_find_with_duplicate(self):
    l = Listy([1, 4, 6, 6, 6, 8, 9])
    self.assertIn(l.find(6), (2, 3, 4))


if __name__ == '__main__':
  unittest.main()
