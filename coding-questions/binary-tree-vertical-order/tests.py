import unittest


class TestVerticalOrder(unittest.TestCase):
  def test_empty_tree(self):
    self.assertEqual(vertical_order(None), [])

  def test_single_node(self):
    self.assertEqual(vertical_order(TreeNode(9)), [[9]])

  def test_full_tree(self):
    root = TreeNode(1,
                    TreeNode(2, TreeNode(4), TreeNode(5)),
                    TreeNode(3, TreeNode(6), TreeNode(7)))
    self.assertEqual(vertical_order(root), [[4], [2], [1, 5, 6], [3], [7]])

  def test_left_chain(self):
    root = TreeNode(1, TreeNode(2, TreeNode(3)))
    self.assertEqual(vertical_order(root), [[3], [2], [1]])

  def test_right_chain(self):
    root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
    self.assertEqual(vertical_order(root), [[1], [2], [3]])

  def test_ties_are_top_to_bottom_then_left_to_right(self):
    # Two nodes collide in column 0 at different depths; the shallower (root)
    # comes first, then the deeper one.
    root = TreeNode(1, TreeNode(2, None, TreeNode(3)))
    # columns: -1 -> [2], 0 -> [1, 3]
    self.assertEqual(vertical_order(root), [[2], [1, 3]])

  def test_negative_values(self):
    root = TreeNode(-5, TreeNode(-10), TreeNode(0))
    self.assertEqual(vertical_order(root), [[-10], [-5], [0]])


if __name__ == '__main__':
  unittest.main()
