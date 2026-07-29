# Remove Dups
# Difficulty: easy
# Tags: #linked-list #hashtable #runner
#
# You are given the head node of a singly linked list. Remove all nodes that
# hold a duplicate value so that each value appears at most once. The relative
# order of the first occurrence of each value must be preserved. Mutate the
# list in place.
#
# Input: the head Node of a singly linked list (each node has `value` and
#        `next`).
# Output: the same head node, with duplicate-valued nodes unlinked.
#
# Examples:
#   1 -> 2 -> 2 -> 3      =>  1 -> 2 -> 3
#   1 -> 1 -> 1 -> 1      =>  1
#   4 -> 3 -> 2 -> 1      =>  4 -> 3 -> 2 -> 1  (already unique)
#   5                     =>  5  (single node)
#
# Approach: keep a hash set of values already seen; walk the list with a
# `previous` pointer and splice out any node whose value is already in the set.

import unittest


class Node(object):
  def __init__(self, value):
    self.value = value
    self.next = None

  def append(self, value):
    n = self
    while n.next:
      n = n.next
    n.next = Node(value)

  def dedup(self):
    seen = {self.value}
    previous = self
    n = self.next
    while n:
      if n.value in seen:
        previous.next = n.next
      else:
        seen.add(n.value)
        previous = n
      n = n.next
    return self


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
