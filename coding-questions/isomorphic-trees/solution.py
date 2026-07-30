class Node:
  def __init__(self, data, left=None, right=None):
    self.data = data
    self.left = left
    self.right = right


def is_isomorphic(a, b):
  if a is None and b is None:
    return True
  if a is None or b is None:
    return False
  if a.data != b.data:
    return False
  return (is_isomorphic(a.left, b.left) and is_isomorphic(a.right, b.right)) or \
         (is_isomorphic(a.left, b.right) and is_isomorphic(a.right, b.left))
