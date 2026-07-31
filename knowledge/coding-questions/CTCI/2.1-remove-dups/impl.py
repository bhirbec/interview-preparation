# Remove Dups
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
    # TODO: implement
    raise NotImplementedError
