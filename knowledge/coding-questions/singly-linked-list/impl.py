# Implement a Singly Linked List
#
# Build a singly linked list from scratch, keeping both a head and a tail
# pointer plus a cached element count so size(), push_back() and back() are all
# O(1). Nodes hold a value and a single `next` pointer -- no `prev`.
#
# Required API:
#   size()                - number of elements in the list (O(1))
#   empty()               - True when the list holds no elements
#   value_at(index)       - value of the index-th node, counting from 0 at the
#                           front; IndexError when out of range
#   push_front(value)     - add a node at the front
#   pop_front()           - remove the front node and return its value;
#                           IndexError when the list is empty
#   push_back(value)      - add a node at the end
#   pop_back()            - remove the last node and return its value;
#                           IndexError when the list is empty
#   front()               - value of the first node; IndexError when empty
#   back()                - value of the last node; IndexError when empty
#   insert(index, value)  - insert a node so that it ends up at `index`;
#                           index == size() appends
#   erase(index)          - remove the node at index and return its value
#   value_n_from_end(n)   - value of the n-th node counting back from the end,
#                           where n == 1 is the last node; IndexError when out
#                           of range
#   reverse()             - reverse the list in place (head and tail swap)
#   remove_value(value)   - remove the first node holding this value and return
#                           True; return False if no node holds it
#
# Examples:
#   lst = LinkedList()
#   lst.empty()                 -> True
#   lst.push_back(1); lst.push_back(2); lst.push_front(0)
#   lst.size()                  -> 3            (list is 0 -> 1 -> 2)
#   lst.front(), lst.back()     -> 0, 2
#   lst.value_at(1)             -> 1
#   lst.value_n_from_end(1)     -> 2
#   lst.value_n_from_end(3)     -> 0
#   lst.insert(1, 9)            -> list is 0 -> 9 -> 1 -> 2
#   lst.erase(1)                -> 9,  list is 0 -> 1 -> 2
#   lst.reverse()               -> list is 2 -> 1 -> 0
#   lst.remove_value(1)         -> True,  list is 2 -> 0
#   lst.pop_front(), lst.pop_back() -> 2, 0


class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next = next_node


class LinkedList:
  def __init__(self):
    # TODO: implement
    raise NotImplementedError

  def size(self):
    # TODO: implement
    raise NotImplementedError

  def empty(self):
    # TODO: implement
    raise NotImplementedError

  def value_at(self, index):
    # TODO: implement
    raise NotImplementedError

  def push_front(self, value):
    # TODO: implement
    raise NotImplementedError

  def pop_front(self):
    # TODO: implement
    raise NotImplementedError

  def push_back(self, value):
    # TODO: implement
    raise NotImplementedError

  def pop_back(self):
    # TODO: implement
    raise NotImplementedError

  def front(self):
    # TODO: implement
    raise NotImplementedError

  def back(self):
    # TODO: implement
    raise NotImplementedError

  def insert(self, index, value):
    # TODO: implement
    raise NotImplementedError

  def erase(self, index):
    # TODO: implement
    raise NotImplementedError

  def value_n_from_end(self, n):
    # TODO: implement
    raise NotImplementedError

  def reverse(self):
    # TODO: implement
    raise NotImplementedError

  def remove_value(self, value):
    # TODO: implement
    raise NotImplementedError
