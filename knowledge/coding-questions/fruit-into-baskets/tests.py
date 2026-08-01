import unittest


def brute_force(fruits):
  best = 0
  for i in range(len(fruits)):
    for j in range(i, len(fruits)):
      if len(set(fruits[i:j + 1])) <= 2:
        best = max(best, j - i + 1)
  return best


class TestTotalFruit(unittest.TestCase):
  def test_two_types_whole_row(self):
    self.assertEqual(total_fruit([1, 2, 1]), 3)

  def test_three_types(self):
    self.assertEqual(total_fruit([0, 1, 2, 2]), 3)

  def test_best_window_in_the_middle(self):
    self.assertEqual(total_fruit([1, 2, 3, 2, 2]), 4)

  def test_longer_example(self):
    self.assertEqual(total_fruit([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]), 5)

  def test_single_tree(self):
    self.assertEqual(total_fruit([7]), 1)

  def test_all_same_type(self):
    self.assertEqual(total_fruit([5, 5, 5, 5]), 4)

  def test_every_tree_a_different_type(self):
    self.assertEqual(total_fruit([1, 2, 3, 4, 5]), 2)

  def test_matches_brute_force(self):
    cases = [
        [1, 1, 2, 2, 3, 3, 4],
        [0, 0, 0, 1, 1, 2, 2, 2, 2],
        [4, 1, 4, 1, 4, 3],
        [1, 2, 1, 3, 1, 2, 1],
        [9],
    ]
    for fruits in cases:
      self.assertEqual(total_fruit(fruits), brute_force(fruits), str(fruits))


if __name__ == '__main__':
  unittest.main()
