import unittest


def build_list(values):
  head = None
  for v in reversed(values):
    head = Node(v, head)
  return head


def to_list(head):
  values = []
  n = head
  while n is not None:
    values.append(n.value)
    n = n.next
  return values


class TestSumLists(unittest.TestCase):
  def test_canonical_example(self):
    l1 = build_list([1, 5, 7])  # 751
    l2 = build_list([5, 6, 9])  # 965
    self.assertEqual(to_list(sum_reversed_linked_list(l1, l2)), [6, 1, 7, 1])

  def test_carry_propagates_to_new_digit(self):
    l1 = build_list([9, 9])  # 99
    l2 = build_list([1])     # 1
    self.assertEqual(to_list(sum_reversed_linked_list(l1, l2)), [0, 0, 1])

  def test_different_lengths(self):
    l1 = build_list([5])     # 5
    l2 = build_list([5, 8])  # 85
    self.assertEqual(to_list(sum_reversed_linked_list(l1, l2)), [0, 9])

  def test_zero_plus_zero(self):
    l1 = build_list([0])
    l2 = build_list([0])
    self.assertEqual(to_list(sum_reversed_linked_list(l1, l2)), [0])

  def test_one_list_empty(self):
    l2 = build_list([4, 2])  # 24
    self.assertEqual(to_list(sum_reversed_linked_list(None, l2)), [4, 2])

  def test_both_empty(self):
    self.assertIsNone(sum_reversed_linked_list(None, None))


if __name__ == '__main__':
  unittest.main()
