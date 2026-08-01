import unittest


class TestMinStack(unittest.TestCase):
  def test_example(self):
    s = MinStack()
    s.push(-2)
    s.push(0)
    s.push(-3)
    self.assertEqual(s.get_min(), -3)
    s.pop()
    self.assertEqual(s.top(), 0)
    self.assertEqual(s.get_min(), -2)

  def test_single_element(self):
    s = MinStack()
    s.push(5)
    self.assertEqual(s.top(), 5)
    self.assertEqual(s.get_min(), 5)

  def test_min_at_bottom_survives_pops(self):
    s = MinStack()
    s.push(1)
    s.push(3)
    s.push(2)
    s.pop()
    s.pop()
    self.assertEqual(s.get_min(), 1)

  def test_decreasing_pushes_update_min(self):
    s = MinStack()
    for v in [5, 4, 3, 2, 1]:
      s.push(v)
      self.assertEqual(s.get_min(), v)

  def test_pop_restores_previous_min(self):
    s = MinStack()
    s.push(2)
    s.push(1)
    self.assertEqual(s.get_min(), 1)
    s.pop()
    self.assertEqual(s.get_min(), 2)

  def test_duplicate_minimums(self):
    s = MinStack()
    s.push(1)
    s.push(1)
    s.pop()
    self.assertEqual(s.get_min(), 1)

  def test_negative_values(self):
    s = MinStack()
    s.push(0)
    s.push(-10)
    s.push(7)
    self.assertEqual(s.get_min(), -10)
    self.assertEqual(s.top(), 7)

  def test_reuse_after_emptying(self):
    s = MinStack()
    s.push(3)
    s.pop()
    s.push(9)
    self.assertEqual(s.top(), 9)
    self.assertEqual(s.get_min(), 9)


if __name__ == '__main__':
  unittest.main()
