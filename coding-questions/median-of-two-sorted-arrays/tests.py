import unittest


def _brute_force(a, b):
  return sorted(a + b)[len(a)]


class TestMedianOfTwoSortedArrays(unittest.TestCase):
  def test_disjoint_blocks(self):
    self.assertEqual(find_median([1, 2, 3, 4], [5, 6, 7, 8]), 5)

  def test_interleaved(self):
    self.assertEqual(find_median([1, 3, 5], [2, 4, 6]), 4)

  def test_single_element_each(self):
    self.assertEqual(find_median([5], [9]), 9)

  def test_single_element_reversed(self):
    self.assertEqual(find_median([9], [5]), 9)

  def test_upper_median_definition(self):
    self.assertEqual(find_median([1, 12, 15, 26, 38], [2, 13, 17, 30, 45]), 17)

  def test_all_identical(self):
    self.assertEqual(find_median([7, 7, 7], [7, 7, 7]), 7)

  def test_b_entirely_below_a(self):
    self.assertEqual(find_median([10, 11, 12], [1, 2, 3]), 10)

  def test_with_duplicates_across_arrays(self):
    self.assertEqual(find_median([1, 2, 2, 4], [2, 3, 3, 5]), _brute_force([1, 2, 2, 4], [2, 3, 3, 5]))

  def test_with_negatives(self):
    a = [-5, -3, 0, 8]
    b = [-4, -1, 2, 9]
    self.assertEqual(find_median(a, b), _brute_force(a, b))

  def test_matches_brute_force_exhaustive_small(self):
    import itertools
    for n in (1, 2, 3, 4):
      for a in itertools.combinations_with_replacement(range(6), n):
        for b in itertools.combinations_with_replacement(range(6), n):
          la, lb = list(a), list(b)
          self.assertEqual(find_median(la, lb), _brute_force(la, lb), (la, lb))


if __name__ == '__main__':
  unittest.main()
