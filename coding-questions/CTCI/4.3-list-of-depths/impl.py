# List of Depths
# Difficulty: medium
# Tags: #tree #bfs #linked-list
#
# You are given a binary tree. Write an algorithm that creates a linked list of
# all the nodes at each depth (so a tree of depth D produces D linked lists).
#
# Input:
#   - A binary tree represented as nested dicts. Each node has a 'value' key and
#     optional 'left' and 'right' keys holding child nodes, e.g.
#     {'value': 1, 'left': {'value': 2}, 'right': {'value': 3}}.
# Output:
#   - A list of LinkedList objects, one per depth (index 0 is the root's depth).
#     Each linked list holds that level's values in left-to-right order.
#
# Constraints:
#   - An empty tree (None) yields an empty list.
#
# Examples:
#   tree = {'value': 1,
#           'left':  {'value': 2, 'left': {'value': 4}, 'right': {'value': 5}},
#           'right': {'value': 3, 'left': {'value': 6}, 'right': {'value': 7}}}
#   [list(l) for l in get_layers(tree)] -> [[1], [2, 3], [4, 5, 6, 7]]
#
#   get_layers({'value': 1}) -> one layer: [[1]]
#   get_layers(None)         -> []
#
# Approach: breadth-first traversal tagging each node with its depth; append
# values to the linked list for that depth, appending (not prepending) so nodes
# keep their left-to-right order.


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
  # TODO: implement
  raise NotImplementedError
