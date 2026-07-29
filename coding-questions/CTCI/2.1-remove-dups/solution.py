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
    seen = {self.value}
    previous = self
    n = self.next
    while n:
      if n.value in seen:
        previous.next = n.next
      else:
        seen.add(n.value)
        previous = n
      n = n.next
    return self
