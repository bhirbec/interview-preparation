# Reverse Linked List
#
# Difficulty: easy
# Tags: #linked-list #recursion
#
# You are given the head node of a singly linked list. Reverse the list so that
# the last node becomes the new head and every `next` pointer points to what was
# previously the node before it. Return the head of the reversed list.
#
# Constraints:
#   - The list may be empty (head is None).
#   - Node values are integers; there are no cycles.
#
# Examples:
#   1 -> 2 -> 3 -> 4 -> 5   =>  5 -> 4 -> 3 -> 2 -> 1
#   1 -> 2                  =>  2 -> 1
#   7                       =>  7           (single node)
#   (empty)                 =>  (empty)
#
# Approach: recurse to the end of the list to obtain the new head, then on the
# way back up flip each pair of pointers so the successor points to its
# predecessor.


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


def reverse(node):
  # TODO: implement
  raise NotImplementedError
