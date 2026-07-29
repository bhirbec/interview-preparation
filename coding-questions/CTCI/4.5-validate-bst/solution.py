class Node():
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def is_bst(n):
  def _f(n, min_val, max_val):
    if n is None:
      return True

    if (min_val is not None and n.value <= min_val) or \
       (max_val is not None and n.value >= max_val):
      return False

    return _f(n.left, min_val, n.value) and _f(n.right, n.value, max_val)

  return _f(n, None, None)
