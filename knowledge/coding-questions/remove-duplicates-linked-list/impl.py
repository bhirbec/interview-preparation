# Remove Duplicates From Unsorted Linked List
#
# You are given the head node of an unsorted singly linked list. Remove every
# node that holds a value already seen earlier in the list, so that each value
# appears exactly once. The first occurrence of each value is kept and the
# relative order of the kept nodes is preserved. Mutate the list in place and
# return its head.
#
# Constraints:
#   - The list may be empty (head is None).
#   - Node values are integers and are not sorted.
#
# Examples:
#   2 -> 12 -> 13 -> 15 -> 13 -> 2 -> 15 -> 2   =>  2 -> 12 -> 13 -> 15
#   1 -> 1 -> 1 -> 1                             =>  1
#   4 -> 3 -> 2 -> 1                             =>  4 -> 3 -> 2 -> 1  (all unique)
#   5                                           =>  5  (single node)
#   (empty)                                     =>  (empty)


class Node:
  def __init__(self, value, next=None):
    self.value = value
    self.next = next

  def append(self, value):
    n = self
    while n.next is not None:
      n = n.next
    n.next = Node(value)
    return n.next


def remove_duplicate(head):
  # TODO: implement
  raise NotImplementedError
