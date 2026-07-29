class Node:
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def is_subtree(n1, n2):
  if n2 is None:
    return True

  d2 = get_depth(n2)

  def f(n):
    if n is None:
      return 0, False

    left, r = f(n.left)
    if r:
      return left, r

    right, r = f(n.right)
    if r:
      return right, r

    d = max(left, right) + 1
    if d == d2:
      return d, compare_tree(n, n2)

    return d, False

  return f(n1)[1]


def get_depth(n):
  if n is None:
    return 0

  left = get_depth(n.left)
  right = get_depth(n.right)
  return max(left, right) + 1


def compare_tree(n1, n2):
  if n1 is None or n2 is None:
    # equal only if both are absent
    return n1 is None and n2 is None

  return (
      n1.value == n2.value
      and compare_tree(n1.left, n2.left)
      and compare_tree(n1.right, n2.right)
  )
