# Points In Triangle
#
# Difficulty: medium
# Tags: #geometry #math #ascend
#
# You are given a triangle in the plane, described by its three vertices
# (x1, y1), (x2, y2) and (x3, y3), and two query points P = (p1, q1) and
# Q = (p2, q2). Determine which of the two query points lie strictly inside the
# triangle.
#
# A point is "strictly inside" only if it is in the interior: points that fall on
# an edge or on a vertex do NOT count as inside.
#
# Return an integer code:
#   0  if the three vertices are collinear (they do not form a real triangle)
#   3  if both P and Q are strictly inside
#   1  if only P is strictly inside
#   2  if only Q is strictly inside
#   4  if neither point is strictly inside
#
# Constraints:
#   - all coordinates are integers
#   - the triangle may be given with vertices in any order (clockwise or
#     counter-clockwise)
#
# Examples:
#   triangle (0,0),(4,0),(0,4)
#     P=(1,1) inside, Q=(2,1) inside            -> 3
#     P=(1,1) inside, Q=(5,5) outside           -> 1
#     P=(5,5) outside, Q=(1,1) inside           -> 2
#     P=(5,5) outside, Q=(9,9) outside          -> 4
#     P=(2,2) on the hypotenuse (edge)          -> not inside
#   triangle (0,0),(1,1),(2,2)  (collinear)     -> 0
#
# Approach: reject degenerate triangles via the vertex cross product, then a
# point is inside iff it lies on the same (strict) side of all three edges.


def points_belong_to_triangle(x1, y1, x2, y2, x3, y3, p1, q1, p2, q2):
  # TODO: implement
  raise NotImplementedError
