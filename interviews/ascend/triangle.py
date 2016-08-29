
def pointsBelongToTriangle(x1, y1, x2, y2, x3, y3, p1, q1, p2, q2):
    # if all the points are on a vertival line then we don't have a triangle
    if y1 == y2 and y2 == y3:
        return 0

    # if all the points are on a horizontal line then we don't have a triangle
    if x1 == x2 and x2 == x3:
        return 0

    # find parameter of y = a.x + b
    a = (y1 - y2) / (x1 - x2)
    b = y1 - a*x1

    # check that all the point are aligned
    y3_line = a*x3 + b
    if y3 == y3_line:
        return 0

    p_inside = point_in_triangle(p1, q1, x1, y1, x2, y2, x3, y3)
    q_inside = point_in_triangle(p2, q2, x1, y1, x2, y2, x3, y3)

    if p_inside and q_inside:
        return 3
    elif p_inside:
        return 1
    elif q_inside:
        return 2
    return 4

def point_in_triangle(x, y, x1, y1, x2, y2, x3, y3):
    b1 = sign(x, y, x1, y1, x2, y2) < 0
    b2 = sign(x, y, x2, y2, x3, y3) < 0
    b3 = sign(x, y, x3, y3, x1, y1) < 0
    return b1 == b2 and b2 == b3

def sign(x1, y1, x2, y2, x3, y3):
    return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)
