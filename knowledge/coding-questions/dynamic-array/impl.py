# Implement a Vector (Dynamic Array)
#
# Build a growable array on top of a fixed-size block of storage, the way
# `std::vector` / Python's `list` work under the hood. You are given a raw
# fixed-length buffer (model it with a plain Python list pre-filled with `None`)
# and you may only read and write slots inside it -- you may not use `append`,
# `insert`, `pop`, slicing or any other list method that resizes for you.
#
# Required API:
#   size()               - number of items stored
#   capacity()           - number of items the current buffer can hold
#   is_empty()           - True when size() == 0
#   at(index)            - item at index; IndexError if out of bounds
#   push(item)           - append at the end
#   insert(index, item)  - insert at index, shifting that item and everything
#                          after it one slot to the right
#   prepend(item)        - insert at index 0
#   pop()                - remove the last item and return it; IndexError when
#                          the array is empty
#   delete(index)        - remove the item at index, shifting everything after
#                          it one slot to the left; returns the removed item
#   remove(item)         - remove *every* occurrence of item (by equality)
#   find(item)           - index of the first occurrence, or -1 if absent
#
# Resizing rules:
#   - the buffer starts at capacity 16
#   - when a push/insert would overflow, double the capacity
#   - after a delete, if size drops to a quarter of capacity or less, halve the
#     capacity; never shrink below the initial capacity of 16
#
# Examples:
#   a = DynamicArray()
#   a.size(), a.capacity(), a.is_empty()   -> 0, 16, True
#   a.push(10); a.push(20); a.prepend(5)
#   a.at(0), a.at(2)                       -> 5, 20
#   a.find(20)                             -> 2
#   a.pop()                                -> 20
#   a.insert(1, 7)                         -> array is now [5, 7, 10]
#   a.remove(7)                            -> array is now [5, 10]


class DynamicArray:
  INITIAL_CAPACITY = 16

  def __init__(self):
    # TODO: implement
    raise NotImplementedError

  def size(self):
    # TODO: implement
    raise NotImplementedError

  def capacity(self):
    # TODO: implement
    raise NotImplementedError

  def is_empty(self):
    # TODO: implement
    raise NotImplementedError

  def at(self, index):
    # TODO: implement
    raise NotImplementedError

  def push(self, item):
    # TODO: implement
    raise NotImplementedError

  def insert(self, index, item):
    # TODO: implement
    raise NotImplementedError

  def prepend(self, item):
    # TODO: implement
    raise NotImplementedError

  def pop(self):
    # TODO: implement
    raise NotImplementedError

  def delete(self, index):
    # TODO: implement
    raise NotImplementedError

  def remove(self, item):
    # TODO: implement
    raise NotImplementedError

  def find(self, item):
    # TODO: implement
    raise NotImplementedError
