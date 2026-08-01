import unittest


def normalized(combinations):
  return sorted(sorted(combo) for combo in combinations)


class TestCombinationSum(unittest.TestCase):
  def test_example(self):
    self.assertEqual(normalized(combination_sum([2, 3, 6, 7], 7)),
                     normalized([[2, 2, 3], [7]]))

  def test_example_multiple_reuses(self):
    self.assertEqual(normalized(combination_sum([2, 3, 5], 8)),
                     normalized([[2, 2, 2, 2], [2, 3, 3], [3, 5]]))

  def test_no_solution(self):
    self.assertEqual(combination_sum([2], 1), [])

  def test_odd_target_with_even_candidates(self):
    self.assertEqual(combination_sum([2, 4], 7), [])

  def test_single_candidate_dividing_target(self):
    self.assertEqual(normalized(combination_sum([3], 9)),
                     normalized([[3, 3, 3]]))

  def test_candidate_equal_to_target(self):
    self.assertEqual(normalized(combination_sum([5, 10], 10)),
                     normalized([[5, 5], [10]]))

  def test_unsorted_candidates(self):
    self.assertEqual(normalized(combination_sum([7, 3, 2], 7)),
                     normalized([[2, 2, 3], [7]]))

  def test_no_duplicate_combinations(self):
    result = combination_sum([2, 3, 4, 5, 6, 7], 10)
    self.assertEqual(len(normalized(result)),
                     len(set(map(tuple, normalized(result)))))

  def test_larger_target(self):
    # Partitions of 12 into parts from {4, 6, 12}.
    self.assertEqual(normalized(combination_sum([4, 6, 12], 12)),
                     normalized([[4, 4, 4], [6, 6], [12]]))


if __name__ == '__main__':
  unittest.main()
