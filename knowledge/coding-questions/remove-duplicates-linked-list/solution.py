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
  seen = set()
  previous = None
  node = head
  while node is not None:
    if node.value in seen:
      previous.next = node.next
      node = previous
    else:
      seen.add(node.value)
      previous = node
    node = node.next
  return head
