import unittest


def _big_tree():
  return Node(
      value=10,
      left=Node(
          value=5,
          left=Node(value=2, left=Node(value=1), right=Node(value=3)),
          right=Node(value=7, left=Node(value=6), right=Node(value=8)),
      ),
      right=Node(value=15, left=Node(value=12), right=Node(value=41)),
  )


class TestCheckSubtree(unittest.TestCase):
  def test_subtree_present(self):
    n1 = _big_tree()
    n2 = Node(value=15, left=Node(value=12), right=Node(value=41))
    self.assertTrue(is_subtree(n1, n2))

  def test_deep_subtree_present(self):
    n1 = _big_tree()
    n2 = Node(value=2, left=Node(value=1), right=Node(value=3))
    self.assertTrue(is_subtree(n1, n2))

  def test_leaf_subtree_present(self):
    n1 = _big_tree()
    self.assertTrue(is_subtree(n1, Node(value=8)))

  def test_root_equals_whole_tree(self):
    n1 = _big_tree()
    n2 = _big_tree()
    self.assertTrue(is_subtree(n1, n2))

  def test_value_mismatch(self):
    n1 = _big_tree()
    n2 = Node(value=15, left=Node(value=12), right=Node(value=99))
    self.assertFalse(is_subtree(n1, n2))

  def test_structure_mismatch(self):
    # 5 in T1 has two children; here T2's 5 has only a left child.
    n1 = _big_tree()
    n2 = Node(value=5, left=Node(value=2))
    self.assertFalse(is_subtree(n1, n2))

  def test_missing_value(self):
    n1 = _big_tree()
    self.assertFalse(is_subtree(n1, Node(value=100)))

  def test_empty_t2_is_subtree(self):
    self.assertTrue(is_subtree(_big_tree(), None))

  def test_empty_t1_non_empty_t2(self):
    self.assertFalse(is_subtree(None, Node(value=1)))

  def test_both_empty(self):
    self.assertTrue(is_subtree(None, None))


if __name__ == '__main__':
  unittest.main()
