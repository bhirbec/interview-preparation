class CircularQueue:
  def __init__(self, capacity):
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
      raise ValueError('capacity must be a positive integer')
    self._capacity = capacity
    self._data = [None] * capacity
    self._head = 0
    self._size = 0

  def enqueue(self, value):
    if self.full():
      raise OverflowError('queue is full')
    # The back of the queue is `size` slots past the head, wrapping around.
    self._data[(self._head + self._size) % self._capacity] = value
    self._size += 1

  def dequeue(self):
    if self.empty():
      raise IndexError('dequeue from an empty queue')
    value = self._data[self._head]
    self._data[self._head] = None
    self._head = (self._head + 1) % self._capacity
    self._size -= 1
    return value

  def peek(self):
    if self.empty():
      raise IndexError('peek at an empty queue')
    return self._data[self._head]

  def empty(self):
    return self._size == 0

  def full(self):
    return self._size == self._capacity

  def size(self):
    return self._size

  def capacity(self):
    return self._capacity
