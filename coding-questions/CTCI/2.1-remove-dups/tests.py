import unittest


def build_list(values):
  head = Node(values[0])
  for v in values[1:]:
    head.append(v)
  return head


def to_list(head):
  values = []
  n = head
  while n:
    values.append(n.value)
    n = n.next
  return values


class TestRemoveDups(unittest.TestCase):
  def test_removes_adjacent_duplicates(self):
    head = build_list([1, 2, 2, 3])
    self.assertEqual(to_list(head.dedup()), [1, 2, 3])

  def test_removes_non_adjacent_duplicates(self):
    head = build_list([1, 2, 3, 2, 1, 4])
    self.assertEqual(to_list(head.dedup()), [1, 2, 3, 4])

  def test_all_same_values(self):
    head = build_list([1, 1, 1, 1])
    self.assertEqual(to_list(head.dedup()), [1])

  def test_already_unique(self):
    head = build_list([4, 3, 2, 1])
    self.assertEqual(to_list(head.dedup()), [4, 3, 2, 1])

  def test_single_node(self):
    head = build_list([5])
    self.assertEqual(to_list(head.dedup()), [5])

  def test_preserves_first_occurrence_order(self):
    head = build_list([3, 1, 3, 2, 1])
    self.assertEqual(to_list(head.dedup()), [3, 1, 2])


if __name__ == '__main__':
  unittest.main()
