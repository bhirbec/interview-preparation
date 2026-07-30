class _Node(object):
  def __init__(self, key, value):
    self.key = key
    self.value = value
    self.prev = None
    self.next = None


class LRUCache(object):
  def __init__(self, capacity):
    self.capacity = capacity
    self.map = {}
    # Sentinel head/tail so insert/remove never hit None edge cases.
    self.head = _Node(None, None)
    self.tail = _Node(None, None)
    self.head.next = self.tail
    self.tail.prev = self.head

  def _remove(self, node):
    node.prev.next = node.next
    node.next.prev = node.prev

  def _add_front(self, node):
    node.prev = self.head
    node.next = self.head.next
    self.head.next.prev = node
    self.head.next = node

  def get(self, key):
    node = self.map.get(key)
    if node is None:
      return -1
    self._remove(node)
    self._add_front(node)
    return node.value

  def put(self, key, value):
    node = self.map.get(key)
    if node is not None:
      node.value = value
      self._remove(node)
      self._add_front(node)
      return

    if len(self.map) == self.capacity:
      lru = self.tail.prev
      self._remove(lru)
      del self.map[lru.key]

    node = _Node(key, value)
    self.map[key] = node
    self._add_front(node)
