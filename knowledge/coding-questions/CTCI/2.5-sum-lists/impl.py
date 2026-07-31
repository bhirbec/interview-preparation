# Sum Lists
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


class Node:
  def __init__(self, value, next=None):
    self.value = value
    self.next = next


def sum_reversed_linked_list(l1, l2):
  # TODO: implement
  raise NotImplementedError
