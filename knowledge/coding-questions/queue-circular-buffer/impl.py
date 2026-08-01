# Implement a Queue with a Fixed-Size Circular Buffer
#
# Implement a FIFO queue on top of a fixed-size array (a ring buffer). Allocate
# the storage once in the constructor and never grow it: model it with a plain
# Python list pre-filled with `None`, and only read and write slots inside it.
# You may not use `append`, `pop`, `insert` or slicing.
#
# The trick is to track where the front of the queue currently lives and how
# many items are stored, and to wrap both the read and the write position back
# around to 0 when they run off the end of the storage.
#
# Required API:
#   CircularQueue(capacity) - allocate storage for `capacity` items;
#                             ValueError if capacity is not a positive integer
#   enqueue(value)          - add at the back; OverflowError when full
#   dequeue()               - remove and return the least recently added item;
#                             IndexError when empty
#   peek()                  - the least recently added item without removing it;
#                             IndexError when empty
#   empty()                 - True when the queue holds no items
#   full()                  - True when the queue holds `capacity` items
#   size()                  - number of items currently queued
#   capacity()              - the fixed storage size
#
# Examples:
#   q = CircularQueue(3)
#   q.empty(), q.full(), q.size()   -> True, False, 0
#   q.enqueue('a'); q.enqueue('b'); q.enqueue('c')
#   q.full()                        -> True
#   q.dequeue()                     -> 'a'
#   q.enqueue('d')                  -> reuses the slot 'a' just vacated
#   q.peek()                        -> 'b'
#   q.dequeue(), q.dequeue(), q.dequeue()  -> 'b', 'c', 'd'
#   q.empty()                       -> True


class CircularQueue:
  def __init__(self, capacity):
    # TODO: implement
    raise NotImplementedError

  def enqueue(self, value):
    # TODO: implement
    raise NotImplementedError

  def dequeue(self):
    # TODO: implement
    raise NotImplementedError

  def peek(self):
    # TODO: implement
    raise NotImplementedError

  def empty(self):
    # TODO: implement
    raise NotImplementedError

  def full(self):
    # TODO: implement
    raise NotImplementedError

  def size(self):
    # TODO: implement
    raise NotImplementedError

  def capacity(self):
    # TODO: implement
    raise NotImplementedError
