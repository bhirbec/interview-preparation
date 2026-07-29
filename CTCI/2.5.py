# Sum Lists
# Difficulty: medium
# Tags: #linked-list #math #recursion
#
# You are given two numbers represented as singly linked lists, where each node
# holds a single digit and the digits are stored in reverse order (the 1's
# digit is at the head of the list). Add the two numbers and return the sum as
# a linked list in the same reverse-order format.
#
# Input: two head Nodes l1 and l2 (each node has `value` in 0..9 and `next`).
#        Either list may be shorter than the other; a None list represents 0.
# Output: the head Node of a linked list holding the digits of the sum, least
#         significant digit first.
#
# Examples:
#   (1 -> 5 -> 7) + (5 -> 6 -> 9)   =>  6 -> 1 -> 7 -> 1
#     i.e. 751 + 965 = 1716
#   (0) + (0)                       =>  0
#   (9 -> 9) + (1)                  =>  0 -> 0 -> 1   (99 + 1 = 100)
#   (5) + (5 -> 8)                  =>  0 -> 9        (5 + 85 = 90)
#
# Approach: recurse over both lists together, summing digit values plus the
# incoming carry, emitting `sum % 10` and propagating `sum // 10` as the carry
# into the next recursive call; stop only when both lists and the carry are
# exhausted.

import unittest


class Node:
  def __init__(self, value, next=None):
    self.value = value
    self.next = next


def sum_reversed_linked_list(l1, l2):
  def _f(l1, l2, carry):
    if l1 is None and l2 is None and carry == 0:
      return None

    v = carry
    l1_next = None
    l2_next = None

    if l1 is not None:
      l1_next = l1.next
      v += l1.value

    if l2 is not None:
      l2_next = l2.next
      v += l2.value

    carry = 1 if v > 9 else 0
    n = Node(v % 10, _f(l1_next, l2_next, carry))
    return n

  return _f(l1, l2, 0)


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
