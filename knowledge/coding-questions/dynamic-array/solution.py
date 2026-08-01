class DynamicArray:
  INITIAL_CAPACITY = 16

  def __init__(self):
    self._capacity = self.INITIAL_CAPACITY
    self._size = 0
    self._data = [None] * self._capacity

  def size(self):
    return self._size

  def capacity(self):
    return self._capacity

  def is_empty(self):
    return self._size == 0

  def at(self, index):
    if index < 0 or index >= self._size:
      raise IndexError('index out of range: %r' % (index,))
    return self._data[index]

  def push(self, item):
    self.insert(self._size, item)

  def insert(self, index, item):
    if index < 0 or index > self._size:
      raise IndexError('index out of range: %r' % (index,))
    if self._size == self._capacity:
      self._resize(self._capacity * 2)
    # Shift the tail one slot right, starting from the far end so nothing is
    # overwritten before it has been copied.
    for i in range(self._size, index, -1):
      self._data[i] = self._data[i - 1]
    self._data[index] = item
    self._size += 1

  def prepend(self, item):
    self.insert(0, item)

  def pop(self):
    if self._size == 0:
      raise IndexError('pop from an empty array')
    return self.delete(self._size - 1)

  def delete(self, index):
    if index < 0 or index >= self._size:
      raise IndexError('index out of range: %r' % (index,))
    removed = self._data[index]
    for i in range(index, self._size - 1):
      self._data[i] = self._data[i + 1]
    self._data[self._size - 1] = None
    self._size -= 1
    if self._size * 4 <= self._capacity:
      self._resize(max(self.INITIAL_CAPACITY, self._capacity // 2))
    return removed

  def remove(self, item):
    i = 0
    while i < self._size:
      if self._data[i] == item:
        self.delete(i)
      else:
        i += 1

  def find(self, item):
    for i in range(self._size):
      if self._data[i] == item:
        return i
    return -1

  def _resize(self, new_capacity):
    if new_capacity == self._capacity:
      return
    data = [None] * new_capacity
    for i in range(self._size):
      data[i] = self._data[i]
    self._data = data
    self._capacity = new_capacity
