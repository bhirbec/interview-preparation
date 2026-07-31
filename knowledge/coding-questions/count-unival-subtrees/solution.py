class Node:
  def __init__(self, value, children=None):
    self.value = value
    self.children = children if children is not None else []


def count_unival_subtrees(root):
  count = 0

  def dfs(node):
    nonlocal count
    is_unival = True
    for child in node.children:
      child_unival = dfs(child)
      if not child_unival or child.value != node.value:
        is_unival = False
    if is_unival:
      count += 1
    return is_unival

  if root is None:
    return 0
  dfs(root)
  return count
