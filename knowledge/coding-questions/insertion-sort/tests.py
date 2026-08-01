import unittest


class TestInsertionSort(unittest.TestCase):
  def test_example(self):
    self.assertEqual(insertion_sort([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9])

  def test_empty(self):
    self.assertEqual(insertion_sort([]), [])

  def test_single_element(self):
    self.assertEqual(insertion_sort([1]), [1])

  def test_two_elements(self):
    self.assertEqual(insertion_sort([2, 1]), [1, 2])
    self.assertEqual(insertion_sort([1, 2]), [1, 2])

  def test_already_sorted(self):
    self.assertEqual(insertion_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

  def test_reverse_sorted(self):
    self.assertEqual(insertion_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

  def test_all_equal(self):
    self.assertEqual(insertion_sort([7, 7, 7, 7]), [7, 7, 7, 7])

  def test_duplicates(self):
    self.assertEqual(insertion_sort([3, 1, 3, 2, 1]), [1, 1, 2, 3, 3])

  def test_negatives(self):
    self.assertEqual(insertion_sort([0, -3, 5, -10, 2]), [-10, -3, 0, 2, 5])

  def test_strings(self):
    self.assertEqual(insertion_sort(['pear', 'fig', 'apple']),
                     ['apple', 'fig', 'pear'])

  def test_sorts_in_place_and_returns_the_same_list(self):
    items = [3, 1, 2]
    result = insertion_sort(items)
    self.assertIs(result, items)
    self.assertEqual(items, [1, 2, 3])

  def test_stability(self):
    # Sort (key, tag) pairs by key only; equal keys must keep their input order.
    class ByKey:
      def __init__(self, key, tag):
        self.key = key
        self.tag = tag

      def __lt__(self, other):
        return self.key < other.key

    pairs = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (2, 'e')]
    sorted_pairs = insertion_sort([ByKey(key, tag) for key, tag in pairs])
    self.assertEqual([item.tag for item in sorted_pairs],
                     ['b', 'd', 'a', 'c', 'e'])

  def test_nearly_sorted(self):
    self.assertEqual(insertion_sort([1, 2, 4, 3, 5]), [1, 2, 3, 4, 5])

  def test_larger_shuffled_input(self):
    items = [(i * 7919) % 500 for i in range(500)]
    expected = sorted(items)
    self.assertEqual(insertion_sort(items), expected)


if __name__ == '__main__':
  unittest.main()
