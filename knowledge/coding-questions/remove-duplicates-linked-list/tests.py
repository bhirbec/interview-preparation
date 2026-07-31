import unittest


def build_list(values):
  head = None
  tail = None
  for value in values:
    node = Node(value)
    if head is None:
      head = node
      tail = node
    else:
      tail.next = node
      tail = node
  return head


def to_list(head):
  values = []
  node = head
  while node is not None:
    values.append(node.value)
    node = node.next
  return values


class TestRemoveDuplicate(unittest.TestCase):
  def test_empty_list(self):
    self.assertEqual(to_list(remove_duplicate(build_list([]))), [])

  def test_single_node(self):
    self.assertEqual(to_list(remove_duplicate(build_list([5]))), [5])

  def test_no_duplicates(self):
    self.assertEqual(to_list(remove_duplicate(build_list([4, 3, 2, 1]))), [4, 3, 2, 1])

  def test_all_duplicates(self):
    self.assertEqual(to_list(remove_duplicate(build_list([1, 1, 1, 1]))), [1])

  def test_mixed_duplicates(self):
    self.assertEqual(
      to_list(remove_duplicate(build_list([2, 12, 13, 15, 13, 2, 15, 2]))),
      [2, 12, 13, 15],
    )

  def test_duplicate_at_head(self):
    self.assertEqual(to_list(remove_duplicate(build_list([7, 7, 8, 9]))), [7, 8, 9])

  def test_duplicate_at_tail(self):
    self.assertEqual(to_list(remove_duplicate(build_list([8, 9, 10, 10]))), [8, 9, 10])

  def test_adjacent_and_distant_duplicates(self):
    self.assertEqual(
      to_list(remove_duplicate(build_list([1, 2, 2, 3, 1, 3]))),
      [1, 2, 3],
    )

  def test_tail_terminates(self):
    head = remove_duplicate(build_list([1, 1, 2, 2]))
    node = head
    while node.next is not None:
      node = node.next
    self.assertIsNone(node.next)


if __name__ == '__main__':
  unittest.main()
