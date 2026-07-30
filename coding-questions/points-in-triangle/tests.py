import unittest


class TestPointsBelongToTriangle(unittest.TestCase):
  def test_both_points_inside(self):
    self.assertEqual(
      points_belong_to_triangle(0, 0, 4, 0, 0, 4, 1, 1, 2, 1), 3)

  def test_only_first_point_inside(self):
    self.assertEqual(
      points_belong_to_triangle(0, 0, 4, 0, 0, 4, 1, 1, 5, 5), 1)

  def test_only_second_point_inside(self):
    self.assertEqual(
      points_belong_to_triangle(0, 0, 4, 0, 0, 4, 5, 5, 1, 1), 2)

  def test_neither_point_inside(self):
    self.assertEqual(
      points_belong_to_triangle(0, 0, 4, 0, 0, 4, 5, 5, 9, 9), 4)

  def test_degenerate_collinear_triangle(self):
    self.assertEqual(
      points_belong_to_triangle(0, 0, 1, 1, 2, 2, 1, 1, 0, 0), 0)

  def test_point_on_edge_is_outside(self):
    # (2, 2) lies on the hypotenuse x + y = 4; (2, 0) on the bottom edge.
    self.assertEqual(
      points_belong_to_triangle(0, 0, 4, 0, 0, 4, 2, 2, 2, 0), 4)

  def test_point_on_vertex_is_outside(self):
    self.assertEqual(
      points_belong_to_triangle(0, 0, 4, 0, 0, 4, 0, 0, 4, 0), 4)

  def test_orientation_independent(self):
    # Same triangle with vertices listed clockwise instead of counter-clockwise.
    self.assertEqual(
      points_belong_to_triangle(0, 0, 0, 4, 4, 0, 1, 1, 2, 1), 3)

  def test_negative_coordinates(self):
    self.assertEqual(
      points_belong_to_triangle(-4, -4, 4, -4, 0, 4, 0, 0, -10, -10), 1)


if __name__ == '__main__':
  unittest.main()
