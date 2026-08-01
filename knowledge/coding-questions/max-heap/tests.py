import unittest


def is_max_heap(array):
  for index in range(len(array)):
    for child in (2 * index + 1, 2 * index + 2):
      if child < len(array) and array[child] > array[index]:
        return False
  return True


def drain(heap):
  return [heap.extract_max() for _ in range(heap.get_size())]


class TestMaxHeap(unittest.TestCase):
  def test_starts_empty(self):
    h = MaxHeap()
    self.assertTrue(h.is_empty())
    self.assertEqual(h.get_size(), 0)

  def test_insert_and_get_max(self):
    h = MaxHeap()
    h.insert(3)
    self.assertEqual(h.get_max(), 3)
    h.insert(9)
    self.assertEqual(h.get_max(), 9)
    h.insert(5)
    self.assertEqual(h.get_max(), 9)
    self.assertEqual(h.get_size(), 3)
    self.assertFalse(h.is_empty())

  def test_get_max_does_not_remove(self):
    h = MaxHeap([1, 2])
    self.assertEqual(h.get_max(), 2)
    self.assertEqual(h.get_max(), 2)
    self.assertEqual(h.get_size(), 2)

  def test_extract_max_returns_descending_order(self):
    h = MaxHeap()
    for value in [3, 9, 5, 1, 8, 2]:
      h.insert(value)
    self.assertEqual(drain(h), [9, 8, 5, 3, 2, 1])
    self.assertTrue(h.is_empty())

  def test_heapify_from_an_array(self):
    h = MaxHeap([4, 10, 3, 5, 1])
    self.assertTrue(is_max_heap(h.to_array()))
    self.assertEqual(h.get_max(), 10)
    self.assertEqual(drain(h), [10, 5, 4, 3, 1])

  def test_heap_property_holds_after_every_insert(self):
    h = MaxHeap()
    for value in [5, 1, 9, 2, 8, 3, 7, 4, 6, 0]:
      h.insert(value)
      self.assertTrue(is_max_heap(h.to_array()))
    self.assertEqual(drain(h), list(range(9, -1, -1)))

  def test_heap_property_holds_after_every_extract(self):
    h = MaxHeap([5, 1, 9, 2, 8, 3, 7, 4, 6, 0])
    while not h.is_empty():
      h.extract_max()
      self.assertTrue(is_max_heap(h.to_array()))

  def test_remove_by_index(self):
    h = MaxHeap([9, 8, 7, 6, 5, 4, 3])
    removed = h.remove(3)
    self.assertEqual(h.get_size(), 6)
    self.assertTrue(is_max_heap(h.to_array()))
    self.assertEqual(sorted(h.to_array() + [removed]), [3, 4, 5, 6, 7, 8, 9])

  def test_remove_last_index(self):
    h = MaxHeap([5, 3, 4])
    last = h.remove(h.get_size() - 1)
    self.assertTrue(is_max_heap(h.to_array()))
    self.assertEqual(h.get_size(), 2)
    self.assertEqual(sorted(h.to_array() + [last]), [3, 4, 5])

  def test_remove_can_require_sifting_up(self):
    # This array is already a valid heap, so heapify leaves it alone. Removing
    # index 3 (value 5) drops the last leaf, 82, into a subtree whose root is
    # only 10 -- sifting the hole down is not enough, the moved leaf has to
    # bubble up past its new parent.
    values = [100, 10, 90, 5, 6, 80, 85, 1, 2, 3, 4, 70, 75, 81, 82]
    h = MaxHeap(values)
    self.assertEqual(h.to_array(), values)
    removed = h.remove(3)
    self.assertEqual(removed, 5)
    self.assertTrue(is_max_heap(h.to_array()))
    self.assertEqual(sorted(h.to_array() + [removed]), sorted(values))

  def test_remove_out_of_range(self):
    h = MaxHeap([1, 2, 3])
    with self.assertRaises(IndexError):
      h.remove(3)
    with self.assertRaises(IndexError):
      h.remove(-1)

  def test_operations_on_empty_heap_raise(self):
    h = MaxHeap()
    with self.assertRaises(IndexError):
      h.get_max()
    with self.assertRaises(IndexError):
      h.extract_max()

  def test_single_element(self):
    h = MaxHeap([42])
    self.assertEqual(h.get_max(), 42)
    self.assertEqual(h.extract_max(), 42)
    self.assertTrue(h.is_empty())

  def test_duplicates(self):
    h = MaxHeap([2, 2, 2, 1, 2])
    self.assertEqual(drain(h), [2, 2, 2, 2, 1])

  def test_negative_values(self):
    h = MaxHeap([-5, -1, -9, -3])
    self.assertEqual(drain(h), [-1, -3, -5, -9])

  def test_reusable_after_draining(self):
    h = MaxHeap([1, 2])
    drain(h)
    h.insert(7)
    self.assertEqual(h.get_max(), 7)
    self.assertEqual(h.get_size(), 1)


if __name__ == '__main__':
  unittest.main()
