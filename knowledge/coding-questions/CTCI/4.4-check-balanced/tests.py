import unittest


class TestIsBalanced(unittest.TestCase):
  def test_empty_tree_is_balanced(self):
    self.assertTrue(is_balanced(None))

  def test_single_node_is_balanced(self):
    self.assertTrue(is_balanced({}))

  def test_balanced_full_tree(self):
    def full(depth):
      if depth == 0:
        return {}
      return {'left': full(depth - 1), 'right': full(depth - 1)}
    self.assertTrue(is_balanced(full(4)))

  def test_off_by_one_is_balanced(self):
    # Left subtree height 2, right subtree height 1: differ by exactly one.
    tree = {
        'left': {'left': {}, 'right': {}},
        'right': {'left': {}},
    }
    self.assertTrue(is_balanced(tree))

  def test_unbalanced_left_heavy(self):
    # Degenerate left chain of depth 2, no right subtree: unbalanced.
    tree = {'left': {'left': {}}}
    self.assertFalse(is_balanced(tree))

  def test_unbalanced_deep_in_subtree(self):
    tree = {
        'left': {},
        'right': {'right': {'right': {'right': {}}}},
    }
    self.assertFalse(is_balanced(tree))

  def test_balanced_with_single_child_each_side(self):
    tree = {'left': {}, 'right': {}}
    self.assertTrue(is_balanced(tree))


if __name__ == '__main__':
  unittest.main()
