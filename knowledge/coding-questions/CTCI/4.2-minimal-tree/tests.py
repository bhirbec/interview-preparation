import unittest


def in_order(n):
  """Return the values of the tree via in-order traversal (sorted for a BST)."""
  if n is None:
    return []
  return in_order(n.left) + [n.value] + in_order(n.right)


def height(n):
  if n is None:
    return 0
  return max(height(n.left), height(n.right)) + 1


def is_bst(n, min_val=None, max_val=None):
  if n is None:
    return True
  if (min_val is not None and n.value <= min_val) or \
     (max_val is not None and n.value >= max_val):
    return False
  return is_bst(n.left, min_val, n.value) and is_bst(n.right, n.value, max_val)


class TestMakeBst(unittest.TestCase):
  def test_empty_array_returns_none(self):
    self.assertIsNone(make_bst([]))

  def test_single_element(self):
    root = make_bst([1])
    assert root is not None
    self.assertEqual(root.value, 1)
    self.assertIsNone(root.left)
    self.assertIsNone(root.right)

  def test_in_order_recovers_sorted_array(self):
    array = [1, 2, 3, 4, 5, 6, 7]
    self.assertEqual(in_order(make_bst(array)), array)

  def test_result_is_a_valid_bst(self):
    self.assertTrue(is_bst(make_bst([1, 2, 3, 4, 5, 6, 7])))

  def test_minimal_height_odd(self):
    # 7 elements: minimal height is ceil(log2(8)) = 3.
    self.assertEqual(height(make_bst([1, 2, 3, 4, 5, 6, 7])), 3)

  def test_minimal_height_even(self):
    # 4 elements: minimal height is 3.
    self.assertEqual(height(make_bst([1, 2, 3, 4])), 3)

  def test_two_elements(self):
    root = make_bst([1, 2])
    self.assertEqual(in_order(root), [1, 2])
    self.assertEqual(height(root), 2)


if __name__ == '__main__':
  unittest.main()
