import unittest


def to_list(lst):
  return [lst.value_at(i) for i in range(lst.size())]


def build(values):
  lst = LinkedList()
  for value in values:
    lst.push_back(value)
  return lst


class TestLinkedList(unittest.TestCase):
  def test_starts_empty(self):
    lst = LinkedList()
    self.assertTrue(lst.empty())
    self.assertEqual(lst.size(), 0)

  def test_push_back_and_push_front(self):
    lst = LinkedList()
    lst.push_back(1)
    lst.push_back(2)
    lst.push_front(0)
    self.assertEqual(to_list(lst), [0, 1, 2])
    self.assertEqual(lst.size(), 3)
    self.assertFalse(lst.empty())

  def test_front_and_back(self):
    lst = build([1, 2, 3])
    self.assertEqual(lst.front(), 1)
    self.assertEqual(lst.back(), 3)

  def test_front_and_back_on_empty_raise(self):
    lst = LinkedList()
    with self.assertRaises(IndexError):
      lst.front()
    with self.assertRaises(IndexError):
      lst.back()

  def test_pop_front(self):
    lst = build([1, 2, 3])
    self.assertEqual(lst.pop_front(), 1)
    self.assertEqual(to_list(lst), [2, 3])

  def test_pop_back(self):
    lst = build([1, 2, 3])
    self.assertEqual(lst.pop_back(), 3)
    self.assertEqual(to_list(lst), [1, 2])
    self.assertEqual(lst.back(), 2)

  def test_pop_on_empty_raises(self):
    lst = LinkedList()
    with self.assertRaises(IndexError):
      lst.pop_front()
    with self.assertRaises(IndexError):
      lst.pop_back()

  def test_emptying_the_list_resets_both_ends(self):
    lst = build([1])
    self.assertEqual(lst.pop_back(), 1)
    self.assertTrue(lst.empty())
    lst.push_back(2)
    self.assertEqual(lst.front(), 2)
    self.assertEqual(lst.back(), 2)
    self.assertEqual(to_list(lst), [2])

  def test_value_at_out_of_range(self):
    lst = build([1, 2])
    self.assertEqual(lst.value_at(1), 2)
    with self.assertRaises(IndexError):
      lst.value_at(2)
    with self.assertRaises(IndexError):
      lst.value_at(-1)

  def test_insert_in_the_middle(self):
    lst = build([0, 1, 2])
    lst.insert(1, 9)
    self.assertEqual(to_list(lst), [0, 9, 1, 2])

  def test_insert_at_the_ends(self):
    lst = build([1])
    lst.insert(0, 0)
    lst.insert(2, 2)
    self.assertEqual(to_list(lst), [0, 1, 2])
    self.assertEqual(lst.back(), 2)

  def test_insert_out_of_range(self):
    lst = build([1])
    with self.assertRaises(IndexError):
      lst.insert(2, 'too far')

  def test_erase(self):
    lst = build([0, 1, 2, 3])
    self.assertEqual(lst.erase(1), 1)
    self.assertEqual(to_list(lst), [0, 2, 3])
    self.assertEqual(lst.erase(2), 3)
    self.assertEqual(to_list(lst), [0, 2])
    self.assertEqual(lst.back(), 2)

  def test_erase_out_of_range(self):
    lst = build([1])
    with self.assertRaises(IndexError):
      lst.erase(1)

  def test_value_n_from_end(self):
    lst = build([0, 1, 2])
    self.assertEqual(lst.value_n_from_end(1), 2)
    self.assertEqual(lst.value_n_from_end(2), 1)
    self.assertEqual(lst.value_n_from_end(3), 0)

  def test_value_n_from_end_out_of_range(self):
    lst = build([0, 1, 2])
    with self.assertRaises(IndexError):
      lst.value_n_from_end(0)
    with self.assertRaises(IndexError):
      lst.value_n_from_end(4)

  def test_reverse(self):
    lst = build([1, 2, 3, 4])
    lst.reverse()
    self.assertEqual(to_list(lst), [4, 3, 2, 1])
    self.assertEqual(lst.front(), 4)
    self.assertEqual(lst.back(), 1)
    lst.push_back(0)
    self.assertEqual(to_list(lst), [4, 3, 2, 1, 0])

  def test_reverse_on_empty_and_single(self):
    lst = LinkedList()
    lst.reverse()
    self.assertEqual(to_list(lst), [])
    lst.push_back(7)
    lst.reverse()
    self.assertEqual(to_list(lst), [7])
    self.assertEqual(lst.back(), 7)

  def test_remove_value(self):
    lst = build([1, 2, 3, 2])
    self.assertTrue(lst.remove_value(2))
    self.assertEqual(to_list(lst), [1, 3, 2])
    self.assertFalse(lst.remove_value(99))
    self.assertEqual(to_list(lst), [1, 3, 2])

  def test_remove_value_at_the_tail_moves_tail(self):
    lst = build([1, 2, 3])
    self.assertTrue(lst.remove_value(3))
    self.assertEqual(lst.back(), 2)
    lst.push_back(4)
    self.assertEqual(to_list(lst), [1, 2, 4])

  def test_remove_only_value(self):
    lst = build([5])
    self.assertTrue(lst.remove_value(5))
    self.assertTrue(lst.empty())
    lst.push_front(6)
    self.assertEqual(to_list(lst), [6])
    self.assertEqual(lst.back(), 6)


if __name__ == '__main__':
  unittest.main()
