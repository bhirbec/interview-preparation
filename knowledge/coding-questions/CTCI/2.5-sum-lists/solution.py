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
