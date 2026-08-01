class MaxHeap:
  def __init__(self, items=None):
    self._data = list(items) if items is not None else []
    if self._data:
      self.heapify()

  def insert(self, value):
    self._data.append(value)
    self._sift_up(len(self._data) - 1)

  def get_max(self):
    if not self._data:
      raise IndexError('get_max on an empty heap')
    return self._data[0]

  def extract_max(self):
    if not self._data:
      raise IndexError('extract_max on an empty heap')
    return self.remove(0)

  def remove(self, index):
    if index < 0 or index >= len(self._data):
      raise IndexError('index out of range: %r' % (index,))
    removed = self._data[index]
    last = self._data.pop()
    if index < len(self._data):
      # The last leaf takes the hole; it may be too small or too large for its
      # new position, so try both directions -- only one of them can move it.
      self._data[index] = last
      self._sift_down(index)
      self._sift_up(index)
    return removed

  def heapify(self):
    for index in range(len(self._data) // 2 - 1, -1, -1):
      self._sift_down(index)

  def get_size(self):
    return len(self._data)

  def is_empty(self):
    return not self._data

  def to_array(self):
    return list(self._data)

  def _sift_up(self, index):
    while index > 0:
      parent = (index - 1) // 2
      if self._data[parent] >= self._data[index]:
        return
      self._data[parent], self._data[index] = self._data[index], self._data[parent]
      index = parent

  def _sift_down(self, index):
    count = len(self._data)
    while True:
      largest = index
      for child in (2 * index + 1, 2 * index + 2):
        if child < count and self._data[child] > self._data[largest]:
          largest = child
      if largest == index:
        return
      self._data[index], self._data[largest] = self._data[largest], self._data[index]
      index = largest
