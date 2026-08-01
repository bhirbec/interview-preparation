class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next = next_node


class LinkedList:
  def __init__(self):
    self.head = None
    self.tail = None
    self._size = 0

  def size(self):
    return self._size

  def empty(self):
    return self._size == 0

  def value_at(self, index):
    return self._node_at(index).value

  def push_front(self, value):
    self.head = Node(value, self.head)
    if self.tail is None:
      self.tail = self.head
    self._size += 1

  def pop_front(self):
    if self.head is None:
      raise IndexError('pop_front from an empty list')
    node = self.head
    self.head = node.next
    if self.head is None:
      self.tail = None
    self._size -= 1
    return node.value

  def push_back(self, value):
    node = Node(value)
    if self.tail is None:
      self.head = self.tail = node
    else:
      self.tail.next = node
      self.tail = node
    self._size += 1

  def pop_back(self):
    if self.head is None:
      raise IndexError('pop_back from an empty list')
    return self.erase(self._size - 1)

  def front(self):
    if self.head is None:
      raise IndexError('front of an empty list')
    return self.head.value

  def back(self):
    if self.tail is None:
      raise IndexError('back of an empty list')
    return self.tail.value

  def insert(self, index, value):
    if index < 0 or index > self._size:
      raise IndexError('index out of range: %r' % (index,))
    if index == 0:
      self.push_front(value)
    elif index == self._size:
      self.push_back(value)
    else:
      previous = self._node_at(index - 1)
      previous.next = Node(value, previous.next)
      self._size += 1

  def erase(self, index):
    if index < 0 or index >= self._size:
      raise IndexError('index out of range: %r' % (index,))
    if index == 0:
      return self.pop_front()
    previous = self._node_at(index - 1)
    node = previous.next
    previous.next = node.next
    if node is self.tail:
      self.tail = previous
    self._size -= 1
    return node.value

  def value_n_from_end(self, n):
    if n < 1 or n > self._size:
      raise IndexError('no node %r from the end' % (n,))
    # Runner starts n nodes ahead; when it falls off the end, `node` is there.
    runner = self.head
    for _ in range(n):
      runner = runner.next
    node = self.head
    while runner is not None:
      runner = runner.next
      node = node.next
    return node.value

  def reverse(self):
    previous = None
    node = self.head
    self.tail = self.head
    while node is not None:
      following = node.next
      node.next = previous
      previous = node
      node = following
    self.head = previous

  def remove_value(self, value):
    previous = None
    node = self.head
    while node is not None:
      if node.value == value:
        if previous is None:
          self.head = node.next
        else:
          previous.next = node.next
        if node is self.tail:
          self.tail = previous
        self._size -= 1
        return True
      previous = node
      node = node.next
    return False

  def _node_at(self, index):
    if index < 0 or index >= self._size:
      raise IndexError('index out of range: %r' % (index,))
    node = self.head
    for _ in range(index):
      node = node.next
    return node
