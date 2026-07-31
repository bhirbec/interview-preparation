import unittest


def _valid_tree():
  return Node(
      value=10,
      left=Node(
          value=5,
          left=Node(value=2, left=Node(1), right=Node(3)),
          right=Node(value=7, left=Node(6), right=Node(8)),
      ),
      right=Node(
          value=15,
          left=Node(12),
          right=Node(41),
      ),
  )


class TestIsBst(unittest.TestCase):
  def test_empty_tree_is_valid(self):
    self.assertTrue(is_bst(None))

  def test_single_node_is_valid(self):
    self.assertTrue(is_bst(Node(1)))

  def test_valid_bst(self):
    self.assertTrue(is_bst(_valid_tree()))

  def test_left_child_greater_than_root(self):
    self.assertFalse(is_bst(Node(5, left=Node(6), right=Node(7))))

  def test_right_child_less_than_root(self):
    self.assertFalse(is_bst(Node(5, left=Node(3), right=Node(4))))

  def test_violation_deep_in_right_subtree(self):
    # 6 is a valid child of 15 locally but violates the root bound (< 10).
    tree = Node(
        value=10,
        left=Node(5),
        right=Node(15, left=Node(6), right=Node(20)),
    )
    self.assertFalse(is_bst(tree))

  def test_duplicate_value_is_invalid(self):
    self.assertFalse(is_bst(Node(5, left=Node(5))))

  def test_left_skewed_valid(self):
    self.assertTrue(is_bst(Node(3, left=Node(2, left=Node(1)))))


if __name__ == '__main__':
  unittest.main()
