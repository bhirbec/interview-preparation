import unittest


def to_list(array):
  return [array.at(i) for i in range(array.size())]


class TestDynamicArray(unittest.TestCase):
  def test_starts_empty(self):
    a = DynamicArray()
    self.assertEqual(a.size(), 0)
    self.assertEqual(a.capacity(), 16)
    self.assertTrue(a.is_empty())

  def test_push_and_at(self):
    a = DynamicArray()
    a.push(10)
    a.push(20)
    a.push(30)
    self.assertEqual(a.size(), 3)
    self.assertFalse(a.is_empty())
    self.assertEqual(to_list(a), [10, 20, 30])

  def test_prepend_and_insert(self):
    a = DynamicArray()
    a.push(10)
    a.push(30)
    a.prepend(5)
    a.insert(2, 20)
    self.assertEqual(to_list(a), [5, 10, 20, 30])

  def test_insert_at_end_is_push(self):
    a = DynamicArray()
    a.insert(0, 'a')
    a.insert(1, 'b')
    self.assertEqual(to_list(a), ['a', 'b'])

  def test_pop_returns_last(self):
    a = DynamicArray()
    a.push(1)
    a.push(2)
    self.assertEqual(a.pop(), 2)
    self.assertEqual(to_list(a), [1])

  def test_pop_on_empty_raises(self):
    a = DynamicArray()
    with self.assertRaises(IndexError):
      a.pop()

  def test_delete_shifts_left(self):
    a = DynamicArray()
    for value in [1, 2, 3, 4]:
      a.push(value)
    self.assertEqual(a.delete(1), 2)
    self.assertEqual(to_list(a), [1, 3, 4])

  def test_remove_deletes_every_occurrence(self):
    a = DynamicArray()
    for value in [7, 1, 7, 2, 7]:
      a.push(value)
    a.remove(7)
    self.assertEqual(to_list(a), [1, 2])

  def test_remove_missing_value_is_a_noop(self):
    a = DynamicArray()
    a.push(1)
    a.remove(99)
    self.assertEqual(to_list(a), [1])

  def test_find(self):
    a = DynamicArray()
    for value in ['x', 'y', 'x']:
      a.push(value)
    self.assertEqual(a.find('x'), 0)
    self.assertEqual(a.find('y'), 1)
    self.assertEqual(a.find('z'), -1)

  def test_out_of_bounds_access(self):
    a = DynamicArray()
    a.push(1)
    with self.assertRaises(IndexError):
      a.at(1)
    with self.assertRaises(IndexError):
      a.at(-1)
    with self.assertRaises(IndexError):
      a.delete(1)
    with self.assertRaises(IndexError):
      a.insert(2, 'too far')

  def test_capacity_doubles_on_overflow(self):
    a = DynamicArray()
    for value in range(16):
      a.push(value)
    self.assertEqual(a.capacity(), 16)
    a.push(16)
    self.assertEqual(a.capacity(), 32)
    self.assertEqual(a.size(), 17)
    self.assertEqual(to_list(a), list(range(17)))

  def test_capacity_halves_when_a_quarter_full(self):
    a = DynamicArray()
    for value in range(17):
      a.push(value)
    self.assertEqual(a.capacity(), 32)
    while a.size() > 8:
      a.pop()
    self.assertEqual(a.capacity(), 16)
    self.assertEqual(to_list(a), list(range(8)))

  def test_capacity_never_drops_below_initial(self):
    a = DynamicArray()
    a.push(1)
    a.pop()
    self.assertEqual(a.capacity(), 16)

  def test_grow_then_shrink_preserves_contents(self):
    a = DynamicArray()
    for value in range(100):
      a.push(value)
    self.assertEqual(to_list(a), list(range(100)))
    for _ in range(90):
      a.pop()
    self.assertEqual(to_list(a), list(range(10)))
    self.assertEqual(a.size(), 10)


if __name__ == '__main__':
  unittest.main()
