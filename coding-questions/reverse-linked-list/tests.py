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


class TestReverse(unittest.TestCase):
  def test_empty_list(self):
    self.assertEqual(to_list(reverse(build_list([]))), [])

  def test_single_node(self):
    self.assertEqual(to_list(reverse(build_list([7]))), [7])

  def test_two_nodes(self):
    self.assertEqual(to_list(reverse(build_list([1, 2]))), [2, 1])

  def test_odd_length(self):
    self.assertEqual(to_list(reverse(build_list([1, 2, 3, 4, 5]))), [5, 4, 3, 2, 1])

  def test_even_length(self):
    self.assertEqual(to_list(reverse(build_list([1, 2, 3, 4]))), [4, 3, 2, 1])

  def test_duplicate_values(self):
    self.assertEqual(to_list(reverse(build_list([2, 2, 3, 2]))), [2, 3, 2, 2])

  def test_negative_values(self):
    self.assertEqual(to_list(reverse(build_list([-1, 0, -3]))), [-3, 0, -1])

  def test_new_tail_terminates(self):
    reversed_head = reverse(build_list([1, 2, 3]))
    node = reversed_head
    while node.next is not None:
      node = node.next
    self.assertEqual(node.value, 1)
    self.assertIsNone(node.next)


if __name__ == '__main__':
  unittest.main()
