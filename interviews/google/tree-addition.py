# Google interview onsite 02/11/2019

# You're given a Binary Tree structure where each node as an integer. Each
# path of the tree represents a number. Compute the sum of all these numbers

#     1
#    / \
#   3   4
#  /   / \
# 7   2   3
#        / \
#       9   1

# 137 + 142 + 1439 + 1431 = 3149

import unittest

class Node(object):
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def compute_sum(root):
  # here the solution I gave (which is not the best)
  class Counter():
    value = 0

  def _f(node, path):
    path.append(node.value)

    if not node.left and not node.right:
      Counter.value += _serialize_path(path)

    if node.left:
      _f(node.left, path)

    if node.right:
      _f(node.right, path)

    path.pop()

  def _serialize_path(path):
    return int(''.join(str(i) for i in path))

  _f(root, [])
  return Counter.value


class TestComputeSum(unittest.TestCase):
  ROOT = Node(
    value=1,
    left=Node(
      value=3,
      left=Node(7)
    ),
    right=Node(
      value=4,
      left=Node(
        value=2
      ),
      right=Node(
        value=3,
        left=Node(9),
        right=Node(1),
      )
    )
  )

  def test_v1(self):
    total = compute_sum(self.ROOT)
    self.assertTrue(total == 3149)


if __name__ == '__main__':
  unittest.main()

