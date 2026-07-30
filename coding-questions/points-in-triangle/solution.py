def points_belong_to_triangle(x1, y1, x2, y2, x3, y3, p1, q1, p2, q2):
  def cross(ax, ay, bx, by, cx, cy):
    return (ax - cx) * (by - cy) - (bx - cx) * (ay - cy)

  # Degenerate: the three vertices are collinear, so there is no triangle.
  if cross(x1, y1, x2, y2, x3, y3) == 0:
    return 0

  def inside(px, py):
    d1 = cross(px, py, x1, y1, x2, y2)
    d2 = cross(px, py, x2, y2, x3, y3)
    d3 = cross(px, py, x3, y3, x1, y1)
    return (d1 > 0 and d2 > 0 and d3 > 0) or (d1 < 0 and d2 < 0 and d3 < 0)

  p_in = inside(p1, q1)
  q_in = inside(p2, q2)

  if p_in and q_in:
    return 3
  if p_in:
    return 1
  if q_in:
    return 2
  return 4
