import unittest


class TestMergeSort(unittest.TestCase):
  def test_example(self):
    self.assertEqual(merge_sort([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9])

  def test_empty(self):
    self.assertEqual(merge_sort([]), [])

  def test_single_element(self):
    self.assertEqual(merge_sort([1]), [1])

  def test_two_elements(self):
    self.assertEqual(merge_sort([2, 1]), [1, 2])
    self.assertEqual(merge_sort([1, 2]), [1, 2])

  def test_already_sorted(self):
    self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

  def test_reverse_sorted(self):
    self.assertEqual(merge_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

  def test_all_equal(self):
    self.assertEqual(merge_sort([7, 7, 7, 7]), [7, 7, 7, 7])

  def test_duplicates(self):
    self.assertEqual(merge_sort([3, 1, 3, 2, 1]), [1, 1, 2, 3, 3])

  def test_negatives(self):
    self.assertEqual(merge_sort([0, -3, 5, -10, 2]), [-10, -3, 0, 2, 5])

  def test_strings(self):
    self.assertEqual(merge_sort(['pear', 'fig', 'apple']),
                     ['apple', 'fig', 'pear'])

  def test_input_is_not_modified(self):
    items = [3, 1, 2]
    merge_sort(items)
    self.assertEqual(items, [3, 1, 2])

  def test_returns_a_new_list(self):
    items = [1, 2, 3]
    self.assertIsNot(merge_sort(items), items)

  def test_stability(self):
    # Sort (key, tag) pairs by key only; equal keys must keep their input order.
    pairs = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (2, 'e')]
    keyed = [(key, index, tag) for index, (key, tag) in enumerate(pairs)]

    class ByKey:
      def __init__(self, item):
        self.item = item

      def __lt__(self, other):
        return self.item[0] < other.item[0]

    wrapped = merge_sort([ByKey(item) for item in keyed])
    self.assertEqual([w.item[2] for w in wrapped], ['b', 'd', 'a', 'c', 'e'])

  def test_merge_helper(self):
    self.assertEqual(merge([1, 4, 7], [2, 3, 8]), [1, 2, 3, 4, 7, 8])
    self.assertEqual(merge([], [1, 2]), [1, 2])
    self.assertEqual(merge([1, 2], []), [1, 2])
    self.assertEqual(merge([], []), [])

  def test_large_shuffled_input(self):
    items = [(i * 7919) % 1000 for i in range(1000)]
    self.assertEqual(merge_sort(items), sorted(items))


if __name__ == '__main__':
  unittest.main()
