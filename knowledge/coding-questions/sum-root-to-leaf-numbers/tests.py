import unittest


class TestSumRootToLeaf(unittest.TestCase):
  def test_empty_tree(self):
    self.assertEqual(sum_root_to_leaf(None), 0)

  def test_single_node(self):
    self.assertEqual(sum_root_to_leaf(Node(5)), 5)

  def test_single_node_zero(self):
    self.assertEqual(sum_root_to_leaf(Node(0)), 0)

  def test_left_chain(self):
    root = Node(1, left=Node(2, left=Node(3)))
    self.assertEqual(sum_root_to_leaf(root), 123)

  def test_two_leaves(self):
    # 1 -> 2 = 12, 1 -> 3 = 13, total 25
    root = Node(1, left=Node(2), right=Node(3))
    self.assertEqual(sum_root_to_leaf(root), 25)

  def test_given_example(self):
    root = Node(
      value=1,
      left=Node(3, left=Node(7)),
      right=Node(
        4,
        left=Node(2),
        right=Node(3, left=Node(9), right=Node(1)),
      ),
    )
    self.assertEqual(sum_root_to_leaf(root), 3149)

  def test_single_child_not_a_leaf(self):
    # The node with value 2 has one child, so 1->2 is not counted; only the
    # full path 1 -> 2 -> 0 = 120 contributes.
    root = Node(1, left=Node(2, right=Node(0)))
    self.assertEqual(sum_root_to_leaf(root), 120)


if __name__ == '__main__':
  unittest.main()
