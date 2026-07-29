# Return Kth to Last
# Difficulty: easy
# Tags: #linked-list #two-pointers #runner #recursion
#
# You are given the head of a singly linked list and an integer k (1-indexed).
# Return the value of the kth node counting from the end of the list. k = 1
# refers to the last node. If the list has fewer than k nodes (or is empty),
# return None.
#
# Input: head Node of a singly linked list (each node has `value` and
#        `next_node`), and an integer k >= 1.
# Output: the value stored in the kth-to-last node, or None.
#
# Examples:
#   12 -> 10 -> 3 -> 1 -> 156 -> 43, k=2   =>  156
#   12 -> 10 -> 3 -> 1 -> 156 -> 43, k=1   =>  43
#   1 -> 2 -> 3,                     k=3   =>  1
#   1 -> 2 -> 3,                     k=4   =>  None (k > length)
#   None,                            k=2   =>  None
#
# Two approaches are provided: a runner (two-pointer) version that advances a
# lead pointer k steps ahead then moves both until the lead falls off the end,
# and a recursive version that counts nodes from the tail on the way back up.

import unittest


class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node


def find_kth_from_tail_runner(n, k):
  runner = n
  for _ in range(k):
    if runner is None:
      return None
    runner = runner.next_node

  while runner is not None:
    n = n.next_node
    runner = runner.next_node

  if n is None:
    return None
  return n.value


def find_kth_from_tail(n, k):
  def _f(n, k):
    if n is None:
      return None, 0

    k_node, l = _f(n.next_node, k)
    if k_node is not None:
      return k_node, l

    l += 1
    if l == k:
      return n, l

    return None, l

  n, l = _f(n, k)
  if n is None:
    return None
  return n.value


def build_list(values):
  head = None
  for v in reversed(values):
    head = Node(v, head)
  return head


class TestReturnKthToLast(unittest.TestCase):
  def setUp(self):
    self.head = build_list([12, 10, 3, 1, 156, 43])

  def test_runner_second_to_last(self):
    self.assertEqual(find_kth_from_tail_runner(self.head, 2), 156)

  def test_runner_last(self):
    self.assertEqual(find_kth_from_tail_runner(self.head, 1), 43)

  def test_runner_first(self):
    self.assertEqual(find_kth_from_tail_runner(self.head, 6), 12)

  def test_runner_out_of_range(self):
    self.assertIsNone(find_kth_from_tail_runner(build_list([1, 2, 3]), 4))

  def test_runner_empty_list(self):
    self.assertIsNone(find_kth_from_tail_runner(None, 2))

  def test_runner_single_node(self):
    self.assertEqual(find_kth_from_tail_runner(build_list([9]), 1), 9)

  def test_recursive_second_to_last(self):
    self.assertEqual(find_kth_from_tail(self.head, 2), 156)

  def test_recursive_last(self):
    self.assertEqual(find_kth_from_tail(self.head, 1), 43)

  def test_recursive_first(self):
    self.assertEqual(find_kth_from_tail(self.head, 6), 12)

  def test_recursive_out_of_range(self):
    self.assertIsNone(find_kth_from_tail(build_list([1, 2, 3]), 4))

  def test_recursive_empty_list(self):
    self.assertIsNone(find_kth_from_tail(None, 2))

  def test_both_agree_across_all_positions(self):
    for k in range(1, 7):
      self.assertEqual(
          find_kth_from_tail(self.head, k),
          find_kth_from_tail_runner(self.head, k))


if __name__ == '__main__':
  unittest.main()
