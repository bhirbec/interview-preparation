import unittest


class TestQuicksort(unittest.TestCase):
  def test_example(self):
    self.assertEqual(quicksort([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9])

  def test_empty(self):
    self.assertEqual(quicksort([]), [])

  def test_single_element(self):
    self.assertEqual(quicksort([1]), [1])

  def test_two_elements(self):
    self.assertEqual(quicksort([2, 1]), [1, 2])
    self.assertEqual(quicksort([1, 2]), [1, 2])

  def test_already_sorted(self):
    self.assertEqual(quicksort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

  def test_reverse_sorted(self):
    self.assertEqual(quicksort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

  def test_all_equal(self):
    self.assertEqual(quicksort([7, 7, 7, 7]), [7, 7, 7, 7])

  def test_duplicates(self):
    self.assertEqual(quicksort([3, 1, 3, 2, 1]), [1, 1, 2, 3, 3])

  def test_negatives(self):
    self.assertEqual(quicksort([0, -3, 5, -10, 2]), [-10, -3, 0, 2, 5])

  def test_strings(self):
    self.assertEqual(quicksort(['pear', 'fig', 'apple']),
                     ['apple', 'fig', 'pear'])

  def test_sorts_in_place_and_returns_the_same_list(self):
    items = [3, 1, 2]
    result = quicksort(items)
    self.assertIs(result, items)
    self.assertEqual(items, [1, 2, 3])

  def test_partition_places_the_pivot(self):
    items = [5, 2, 9, 1, 5, 6]
    index = partition(items, 0, len(items) - 1)
    pivot = items[index]
    self.assertTrue(all(value <= pivot for value in items[:index]))
    self.assertTrue(all(value >= pivot for value in items[index + 1:]))
    self.assertEqual(sorted(items), [1, 2, 5, 5, 6, 9])

  def test_partition_on_a_subrange_leaves_the_rest_alone(self):
    items = [100, 3, 1, 2, 200]
    partition(items, 1, 3)
    self.assertEqual(items[0], 100)
    self.assertEqual(items[4], 200)
    self.assertEqual(sorted(items[1:4]), [1, 2, 3])

  def test_large_sorted_input_does_not_blow_the_stack(self):
    items = list(range(5000))
    self.assertEqual(quicksort(items), list(range(5000)))

  def test_large_shuffled_input(self):
    items = [(i * 7919) % 1000 for i in range(1000)]
    expected = sorted(items)
    self.assertEqual(quicksort(items), expected)


if __name__ == '__main__':
  unittest.main()
