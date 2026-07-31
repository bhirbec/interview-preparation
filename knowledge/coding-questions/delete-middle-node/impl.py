# Delete Middle Node
#
# Implement an algorithm to delete a node from the middle of a singly linked
# list, given access ONLY to that node (you do not have the head of the list).
# After the call, the target node's value must be gone from the list and every
# other value must remain in its original order.
#
# Constraints:
#   - The given node is not None.
#   - The given node is not the tail (last) node of the list; the tail cannot be
#     deleted with only a reference to it.
#   - Node values are integers.
#
# Examples:
#   1 -> 2 -> [3] -> 4 -> 5,  delete node holding 3   =>  1 -> 2 -> 4 -> 5
#   [1] -> 2 -> 3,            delete node holding 1   =>  2 -> 3
#   1 -> 2 -> 3 -> [4] -> 5,  delete node holding 4   =>  1 -> 2 -> 3 -> 5


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


def delete_node(node):
  # TODO: implement
  raise NotImplementedError
