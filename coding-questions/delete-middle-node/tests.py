import unittest


def build_list(values):
  head = None
  tail = None
  for value in values:
    n = Node(value)
    if head is None:
      head = n
      tail = n
    else:
      tail.next = n
      tail = n
  return head


def node_at(head, index):
  node = head
  for _ in range(index):
    node = node.next
  return node


def to_list(head):
  values = []
  node = head
  while node is not None:
    values.append(node.value)
    node = node.next
  return values


class TestDeleteNode(unittest.TestCase):
  def test_delete_middle_node(self):
    head = build_list([1, 2, 3, 4, 5])
    delete_node(node_at(head, 2))
    self.assertEqual(to_list(head), [1, 2, 4, 5])

  def test_delete_head_node(self):
    head = build_list([1, 2, 3])
    delete_node(node_at(head, 0))
    self.assertEqual(to_list(head), [2, 3])

  def test_delete_second_to_last_node(self):
    head = build_list([1, 2, 3, 4, 5])
    delete_node(node_at(head, 3))
    self.assertEqual(to_list(head), [1, 2, 3, 5])

  def test_delete_from_two_node_list(self):
    head = build_list([9, 8])
    delete_node(node_at(head, 0))
    self.assertEqual(to_list(head), [8])

  def test_delete_with_duplicate_values(self):
    head = build_list([5, 5, 5, 5])
    delete_node(node_at(head, 1))
    self.assertEqual(to_list(head), [5, 5, 5])

  def test_deleting_tail_is_unsupported(self):
    head = build_list([1, 2, 3])
    with self.assertRaises(AttributeError):
      delete_node(node_at(head, 2))


if __name__ == '__main__':
  unittest.main()
