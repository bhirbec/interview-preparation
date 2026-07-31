# LRU Cache
#
# Source: https://careercup.com/question?id=5674107183038464
#
# Design a Least Recently Used (LRU) cache with a fixed positive `capacity`,
# supporting two operations, each in O(1) average time:
#   - get(key): return the value for `key`, or -1 if it is not present. A
#     successful get counts as a use of `key`.
#   - put(key, value): insert or update `key` with `value`. If inserting a new
#     key would exceed `capacity`, first evict the least recently used key.
#
# The "least recently used" key is the one whose most recent get/put happened
# furthest in the past.
#
# Constraints:
#   - 1 <= capacity
#   - keys and values are integers
#
# Examples:
#   c = LRUCache(2)
#   c.put(1, 1); c.put(2, 2)
#   c.get(1)        -> 1          (1 is now most recently used)
#   c.put(3, 3)                   (capacity exceeded, evicts key 2)
#   c.get(2)        -> -1         (2 was evicted)
#   c.put(4, 4)                   (evicts key 1)
#   c.get(1)        -> -1
#   c.get(3)        -> 3
#   c.get(4)        -> 4


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

  def get(self, key):
    # TODO: implement
    raise NotImplementedError

  def put(self, key, value):
    # TODO: implement
    raise NotImplementedError
