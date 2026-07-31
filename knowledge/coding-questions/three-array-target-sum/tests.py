import unittest


class TestTargetSum(unittest.TestCase):
  def test_given_example_count(self):
    a = [1, 2, 3, 3]
    b = [2, 3, 3, 4]
    c = [1, 2, 2, 2]
    result = target_sum(a, b, c, 7)
    self.assertEqual(len(result), 20)
    for triple in result:
      self.assertEqual(sum(triple), 7)

  def test_given_example_contents(self):
    a = [1, 2, 3, 3]
    b = [2, 3, 3, 4]
    c = [1, 2, 2, 2]
    expected = (
      [[2, 4, 1]] + [[3, 3, 1]] * 4 +   # z = 1 needs a+b = 6
      ([[1, 4, 2]] + [[2, 3, 2]] * 2 + [[3, 2, 2]] * 2) * 3)  # z = 2 needs 5
    self.assertCountEqual(target_sum(a, b, c, 7), expected)

  def test_single_element_each_match(self):
    self.assertEqual(target_sum([1], [1], [1], 3), [[1, 1, 1]])

  def test_single_element_each_no_match(self):
    self.assertEqual(target_sum([1], [1], [1], 4), [])

  def test_empty_array_yields_no_triples(self):
    self.assertEqual(target_sum([], [1], [1], 2), [])

  def test_no_combination_reaches_target(self):
    self.assertEqual(target_sum([1, 2], [1, 2], [1, 2], 100), [])

  def test_negative_numbers(self):
    result = target_sum([-1, 2], [0, -2], [0, 1, 3], 0)
    self.assertCountEqual(result, [[-1, 0, 1], [-1, -2, 3], [2, -2, 0]])

  def test_duplicates_produce_repeated_triples(self):
    result = target_sum([1, 1], [1, 1], [1], 3)
    self.assertCountEqual(result, [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])

  def test_zero_target(self):
    self.assertCountEqual(target_sum([0], [0], [0], 0), [[0, 0, 0]])


if __name__ == '__main__':
  unittest.main()
