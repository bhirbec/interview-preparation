class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node


def find_intercept(n1, n2):
  if n1 is None or n2 is None:
    return None

  t1, l1 = _get_tail_and_size(n1)
  t2, l2 = _get_tail_and_size(n2)
  if t1 is not t2:
    return None
  elif l1 <= l2:
    return _find_intercept(n1, n2, l2 - l1)
  else:
    return _find_intercept(n2, n1, l1 - l2)


def _find_intercept(shortest, longest, diff):
  for _ in range(diff):
    longest = longest.next_node

  while longest is not shortest:
    longest = longest.next_node
    shortest = shortest.next_node

  return longest


def _get_tail_and_size(n):
  l = 0
  while n.next_node:
    l += 1
    n = n.next_node
  return n, l
