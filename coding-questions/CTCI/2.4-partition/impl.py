# Partition
# Difficulty: medium
# Tags: #linked-list #two-pointers
#
# You are given the head of a singly linked list and a partition value k.
# Rearrange the list so that every node with a value less than k comes before
# every node with a value greater than or equal to k. The partition value k
# itself may appear anywhere in the "greater than or equal" section. Nodes on
# either side of the partition do not need to keep their original relative
# order.
#
# Input: head Node of a singly linked list (each node has `value` and
#        `next_node`), and an integer partition value k.
# Output: the head Node of the rearranged list.
#
# Examples:
#   70 -> 134 -> 3 -> 1 -> 10 -> 9, k=10  =>  9 -> 1 -> 3 -> 70 -> 134 -> 10
#     (all values < 10 precede all values >= 10)
#   1 -> 2 -> 3,                    k=5   =>  all on the "less" side
#   6 -> 7 -> 8,                    k=5   =>  all on the "greater/equal" side
#
# Approach: walk the list once, prepending each node to a `left` list when its
# value < k and to a `right` list otherwise, then splice left in front of right.

import unittest


class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node


def partition(n, k):
  left, right = None, None
  while n:
    next_node = n.next_node

    if n.value >= k:
      n.next_node = right
      right = n
    else:
      n.next_node = left
      left = n

    n = next_node

  if right is None:
    return left
  elif left is None:
    return right

  n = left
  while n.next_node:
    n = n.next_node

  n.next_node = right
  return left


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
