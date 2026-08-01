import unittest


def normalized(points):
  return sorted(map(tuple, points))


class TestKClosest(unittest.TestCase):
  def test_example_k_one(self):
    self.assertEqual(normalized(k_closest([[1, 3], [-2, 2]], 1)),
                     normalized([[-2, 2]]))

  def test_example_k_two(self):
    self.assertEqual(normalized(k_closest([[3, 3], [5, -1], [-2, 4]], 2)),
                     normalized([[3, 3], [-2, 4]]))

  def test_k_equals_len_returns_everything(self):
    points = [[1, 1], [-9, 2], [0, 5]]
    self.assertEqual(normalized(k_closest(points, 3)), normalized(points))

  def test_single_point(self):
    self.assertEqual(k_closest([[2, -3]], 1), [[2, -3]])

  def test_point_at_origin_is_closest(self):
    self.assertEqual(normalized(k_closest([[4, 4], [0, 0], [1, 6]], 1)),
                     normalized([[0, 0]]))

  def test_duplicate_points(self):
    self.assertEqual(normalized(k_closest([[1, 1], [1, 1], [5, 5]], 2)),
                     normalized([[1, 1], [1, 1]]))

  def test_ties_before_the_cutoff_are_kept(self):
    # (0, 2) and (2, 0) tie at distance 4; both beat (3, 3).
    self.assertEqual(normalized(k_closest([[3, 3], [0, 2], [2, 0]], 2)),
                     normalized([[0, 2], [2, 0]]))

  def test_negative_coordinates(self):
    self.assertEqual(normalized(k_closest([[-1, -2], [-4, 0], [3, 3]], 2)),
                     normalized([[-1, -2], [-4, 0]]))

  def test_larger_input(self):
    points = [[i, i] for i in range(1, 101)]
    self.assertEqual(normalized(k_closest(points, 5)),
                     normalized([[i, i] for i in range(1, 6)]))


if __name__ == '__main__':
  unittest.main()
