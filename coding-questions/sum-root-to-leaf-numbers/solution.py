class Node(object):
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def sum_root_to_leaf(root):
  def dfs(node, current):
    if node is None:
      return 0
    current = current * 10 + node.value
    if node.left is None and node.right is None:
      return current
    return dfs(node.left, current) + dfs(node.right, current)

  return dfs(root, 0)
