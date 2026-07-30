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
  if node is None or node.next is None:
    return node
  next_node = node.next
  new_head = reverse(next_node)
  node.next = None
  next_node.next = node
  return new_head
