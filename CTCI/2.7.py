# Intersection
# Difficulty: medium
# Tags: #linked-list #two-pointers #runner
#
# You are given the heads of two singly linked lists. Determine whether the two
# lists intersect, and if they do, return the node at which the intersection
# begins. Intersection is defined by reference (identity), not by value: two
# lists intersect when they share a physical node, after which they run through
# the same tail. If the lists do not intersect, return None.
#
# Input: two head Nodes n1 and n2 (each node has `value` and `next_node`).
# Output: the shared intersection Node, or None if the lists are disjoint.
#
# Examples:
#   n1: 70 -> 134 -> 3 -> 1 -> 10 -> 9 -\
#                                        721 -> 12 -> 33   => intersects at 721
#   n2:                     7 -> 11 ----/
#
#   Two fully separate lists                              => None
#   Both heads being the same node                        => that node
#
# Approach: walk each list to find its tail and length. If the tails are not
# the same object the lists cannot intersect. Otherwise advance a pointer in
# the longer list by the length difference, then advance both pointers in
# lockstep until they reference the same node -- that node is the intersection.

import unittest


class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node


def find_intercept(n1, n2):
  if n1 is None or n2 is None:
    return None

  t1, l1 = _get_tail_and_size(n1)
  t2, l2 = _get_tail_and_size(n2)
  if t1 is not t2:
    return None
  elif l1 <= l2:
    return _find_intercept(n1, n2, l2 - l1)
  else:
    return _find_intercept(n2, n1, l1 - l2)


def _find_intercept(shortest, longest, diff):
  for _ in range(diff):
    longest = longest.next_node

  while longest is not shortest:
    longest = longest.next_node
    shortest = shortest.next_node

  return longest


def _get_tail_and_size(n):
  l = 0
  while n.next_node:
    l += 1
    n = n.next_node
  return n, l


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
