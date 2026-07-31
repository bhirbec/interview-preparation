import unittest


class TestCountUnivalSubtrees(unittest.TestCase):
  def test_empty_tree(self):
    self.assertEqual(count_unival_subtrees(None), 0)

  def test_single_node(self):
    self.assertEqual(count_unival_subtrees(Node(7)), 1)

  def test_root_with_all_matching_children(self):
    root = Node(1, [Node(1), Node(1), Node(1)])
    self.assertEqual(count_unival_subtrees(root), 4)

  def test_root_with_two_matching_children(self):
    root = Node(1, [Node(1), Node(1)])
    self.assertEqual(count_unival_subtrees(root), 3)

  def test_mixed_tree(self):
    # root 1 -> [ node 1 -> [node 2], node 1 (leaf) ]
    a = Node(1, [Node(2)])
    b = Node(1)
    root = Node(1, [a, b])
    self.assertEqual(count_unival_subtrees(root), 2)

  def test_no_unival_above_leaves(self):
    # Every internal node differs from its children -> only the leaves count.
    root = Node(1, [Node(2, [Node(3)]), Node(4)])
    self.assertEqual(count_unival_subtrees(root), 2)

  def test_deep_uniform_chain(self):
    # A single chain of identical values: every node roots a unival subtree.
    leaf = Node(5)
    mid = Node(5, [leaf])
    root = Node(5, [mid])
    self.assertEqual(count_unival_subtrees(root), 3)

  def test_one_deviating_leaf_breaks_ancestors(self):
    # root 9 -> child 9 -> [9, 8]; the 8 breaks its parent and the root.
    root = Node(9, [Node(9, [Node(9), Node(8)])])
    self.assertEqual(count_unival_subtrees(root), 2)


if __name__ == '__main__':
  unittest.main()
