from queue import Queue


class LinkedList():

  class _Node():
    def __init__(self, value, next_node=None):
      self.value = value
      self.next_node = next_node

  def __init__(self, value):
    n = self._Node(value)
    self._head = n
    self._tail = n

  def append(self, value):
    n = self._Node(value)
    self._tail.next_node = n
    self._tail = n

  def insert(self, value):
    n = self._Node(value, self._head)
    self._head = n

  def __str__(self):
    return ', '.join(str(v) for v in self)

  def __iter__(self):
    n = self._head
    while n is not None:
      yield n.value
      n = n.next_node


def get_layers(root):
  if root is None:
    return []

  q = Queue()
  q.put((root, 0))
  layers = []

  while not q.empty():
    n, d = q.get()

    if len(layers) == d:
      layers.append(LinkedList(n['value']))
    else:
      # Append (not insert) so values stay in left-to-right order.
      layers[d].append(n['value'])

    if 'left' in n:
      q.put((n['left'], d + 1))

    if 'right' in n:
      q.put((n['right'], d + 1))

  return layers
