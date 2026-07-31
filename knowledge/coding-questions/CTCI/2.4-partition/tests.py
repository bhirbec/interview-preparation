import unittest


def build_list(values):
  head = None
  for v in reversed(values):
    head = Node(v, head)
  return head


def to_list(head):
  values = []
  n = head
  while n:
    values.append(n.value)
    n = n.next_node
  return values


def is_partitioned(values, k):
  seen_ge = False
  for v in values:
    if v >= k:
      seen_ge = True
    elif seen_ge:
      return False
  return True


class TestPartition(unittest.TestCase):
  def test_canonical_example_is_partitioned(self):
    result = to_list(partition(build_list([70, 134, 3, 1, 10, 9]), 10))
    self.assertEqual(sorted(result), [1, 3, 9, 10, 70, 134])
    self.assertTrue(is_partitioned(result, 10))

  def test_all_less_than_k(self):
    result = to_list(partition(build_list([1, 2, 3]), 5))
    self.assertEqual(sorted(result), [1, 2, 3])
    self.assertTrue(is_partitioned(result, 5))

  def test_all_greater_or_equal(self):
    result = to_list(partition(build_list([6, 7, 8]), 5))
    self.assertEqual(sorted(result), [6, 7, 8])
    self.assertTrue(is_partitioned(result, 5))

  def test_value_equal_to_k_goes_right(self):
    result = to_list(partition(build_list([5, 1, 5, 2]), 5))
    self.assertEqual(sorted(result), [1, 2, 5, 5])
    self.assertTrue(is_partitioned(result, 5))

  def test_single_node(self):
    self.assertEqual(to_list(partition(build_list([42]), 10)), [42])

  def test_empty_list(self):
    self.assertIsNone(partition(None, 10))


if __name__ == '__main__':
  unittest.main()
