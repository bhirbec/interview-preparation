import unittest


def build_list(values, tail=None):
  head = tail
  for v in reversed(values):
    head = Node(v, head)
  return head


class TestIntersection(unittest.TestCase):
  def test_canonical_intersection(self):
    common = Node(721, Node(12, Node(33)))
    n1 = build_list([70, 134, 3, 1, 10, 9], common)
    n2 = build_list([7, 11], common)
    result = find_intercept(n1, n2)
    self.assertIs(result, common)
    assert result is not None
    self.assertEqual(result.value, 721)

  def test_no_intersection(self):
    n1 = build_list([1, 2, 3])
    n2 = build_list([4, 5, 6])
    self.assertIsNone(find_intercept(n1, n2))

  def test_same_value_tails_but_distinct_nodes(self):
    n1 = build_list([1, 2, 33])
    n2 = build_list([9, 33])
    self.assertIsNone(find_intercept(n1, n2))

  def test_intersection_at_head_shared_node(self):
    common = Node(5, Node(6))
    self.assertIs(find_intercept(common, common), common)

  def test_intersection_when_second_list_is_longer(self):
    common = Node(100, Node(200))
    n1 = build_list([1], common)
    n2 = build_list([1, 2, 3, 4], common)
    self.assertIs(find_intercept(n1, n2), common)

  def test_one_list_none(self):
    n1 = build_list([1, 2, 3])
    self.assertIsNone(find_intercept(n1, None))


if __name__ == '__main__':
  unittest.main()
