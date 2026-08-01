# Implement a Max-Heap
#
# Build a binary max-heap stored in a flat array. For the node at index i the
# children live at 2i+1 and 2i+2 and the parent at (i-1)//2, so the tree shape
# is implicit and no node objects are needed.
#
# The heap invariant is that every node is >= both of its children, which puts
# the maximum at index 0. Restoring it after a change is done by sift_up (a new
# leaf bubbles towards the root) or sift_down (a node that is too small sinks
# towards the leaves).
#
# You may not use `heapq`, `sorted`, `max` or `min` -- write the sifting.
#
# Required API:
#   MaxHeap(items=None)  - build a heap; when items are given, heapify them
#   insert(value)        - add a value, keeping the heap property
#   get_max()            - the largest value, without removing it;
#                          IndexError when the heap is empty
#   extract_max()        - remove and return the largest value;
#                          IndexError when the heap is empty
#   remove(index)        - remove and return the value at array index `index`;
#                          IndexError when the index is out of range
#   heapify()            - restore the heap property over the whole array in
#                          O(n), by sifting down every internal node from the
#                          last one back to the root
#   get_size()           - number of values stored
#   is_empty()           - True when the heap holds no values
#   to_array()           - the backing array, for inspection
#
# Examples:
#   h = MaxHeap()
#   h.is_empty()                  -> True
#   h.insert(3); h.insert(9); h.insert(5)
#   h.get_max(), h.get_size()     -> 9, 3
#   h.extract_max()               -> 9
#   h.extract_max()               -> 5
#
#   h = MaxHeap([4, 10, 3, 5, 1])
#   h.get_max()                   -> 10
#   [h.extract_max() for _ in range(5)]  -> [10, 5, 4, 3, 1]


class MaxHeap:
  def __init__(self, items=None):
    # TODO: implement
    raise NotImplementedError

  def insert(self, value):
    # TODO: implement
    raise NotImplementedError

  def get_max(self):
    # TODO: implement
    raise NotImplementedError

  def extract_max(self):
    # TODO: implement
    raise NotImplementedError

  def remove(self, index):
    # TODO: implement
    raise NotImplementedError

  def heapify(self):
    # TODO: implement
    raise NotImplementedError

  def get_size(self):
    # TODO: implement
    raise NotImplementedError

  def is_empty(self):
    # TODO: implement
    raise NotImplementedError

  def to_array(self):
    # TODO: implement
    raise NotImplementedError

  def _sift_up(self, index):
    # TODO: implement
    raise NotImplementedError

  def _sift_down(self, index):
    # TODO: implement
    raise NotImplementedError
