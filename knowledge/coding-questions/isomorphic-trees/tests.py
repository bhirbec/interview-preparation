import unittest


class TestIsomorphicTrees(unittest.TestCase):
  def test_swapped_children(self):
    a = Node(12, Node(15), Node(17))
    b = Node(12, Node(17), Node(15))
    self.assertTrue(is_isomorphic(a, b))

  def test_identical_trees(self):
    a = Node(12, Node(15), Node(17))
    b = Node(12, Node(15), Node(17))
    self.assertTrue(is_isomorphic(a, b))

  def test_value_mismatch(self):
    a = Node(12, Node(15), Node(17))
    b = Node(12, Node(15), Node(16))
    self.assertFalse(is_isomorphic(a, b))

  def test_root_value_mismatch(self):
    self.assertFalse(is_isomorphic(Node(1), Node(2)))

  def test_both_empty(self):
    self.assertTrue(is_isomorphic(None, None))

  def test_one_empty(self):
    self.assertFalse(is_isomorphic(Node(1), None))
    self.assertFalse(is_isomorphic(None, Node(1)))

  def test_single_nodes_equal(self):
    self.assertTrue(is_isomorphic(Node(7), Node(7)))

  def test_structural_mismatch_same_values(self):
    # a has a left child only; b has a right child only with the same value.
    a = Node(1, Node(2), None)
    b = Node(1, Node(2), None)
    self.assertTrue(is_isomorphic(a, b))
    c = Node(1, None, Node(2))
    self.assertTrue(is_isomorphic(a, c))

  def test_missing_versus_present_child(self):
    a = Node(1, Node(2), Node(3))
    b = Node(1, Node(2), None)
    self.assertFalse(is_isomorphic(a, b))

  def test_deep_flips(self):
    # Larger trees isomorphic only through flips at multiple levels.
    a = Node(1,
             Node(2, Node(4), Node(5)),
             Node(3, Node(6), None))
    b = Node(1,
             Node(3, None, Node(6)),
             Node(2, Node(5), Node(4)))
    self.assertTrue(is_isomorphic(a, b))

  def test_deep_not_isomorphic(self):
    a = Node(1,
             Node(2, Node(4), Node(5)),
             Node(3))
    b = Node(1,
             Node(2, Node(4), Node(9)),
             Node(3))
    self.assertFalse(is_isomorphic(a, b))


if __name__ == '__main__':
  unittest.main()
