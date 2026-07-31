from collections import deque, defaultdict


class TreeNode:
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def vertical_order(root):
  if root is None:
    return []

  columns = defaultdict(list)
  min_col = 0
  max_col = 0
  q = deque([(root, 0)])

  while q:
    node, col = q.popleft()
    columns[col].append(node.value)
    min_col = min(min_col, col)
    max_col = max(max_col, col)
    if node.left is not None:
      q.append((node.left, col - 1))
    if node.right is not None:
      q.append((node.right, col + 1))

  return [columns[c] for c in range(min_col, max_col + 1)]
