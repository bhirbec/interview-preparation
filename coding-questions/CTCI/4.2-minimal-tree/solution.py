class Node(object):
  def __init__(self, left, right, value):
    self.left = left
    self.right = right
    self.value = value


def make_bst(array):
  n = len(array)
  return _make_bst(array, 0, n - 1)


def _make_bst(array, i, j):
  n = j - i
  if n < 0:
    return None

  mid = i + n // 2
  left = _make_bst(array, i, mid - 1)
  right = _make_bst(array, mid + 1, j)
  return Node(left, right, array[mid])
