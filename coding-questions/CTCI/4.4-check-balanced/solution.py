def is_balanced(n):
  return check_depth(n) != -1


def check_depth(n):
  if n is None:
    return 0

  left = check_depth(n.get('left'))
  if left == -1:
    return -1

  right = check_depth(n.get('right'))
  if right == -1:
    return -1

  diff = abs(left - right)
  if diff > 1:
    return -1

  return max(left, right) + 1
