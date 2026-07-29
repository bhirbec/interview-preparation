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

import unittest
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


class TestGetLayers(unittest.TestCase):
  def _values(self, tree):
    return [list(layer) for layer in get_layers(tree)]

  def test_empty_tree(self):
    self.assertEqual(get_layers(None), [])

  def test_single_node(self):
    self.assertEqual(self._values({'value': 1}), [[1]])

  def test_full_tree_left_to_right_order(self):
    tree = {
        'value': 1,
        'left': {
            'value': 2,
            'left': {'value': 4},
            'right': {'value': 5},
        },
        'right': {
            'value': 3,
            'left': {'value': 6},
            'right': {'value': 7},
        },
    }
    self.assertEqual(self._values(tree), [[1], [2, 3], [4, 5, 6, 7]])

  def test_skewed_left_tree(self):
    tree = {
        'value': 1,
        'left': {'value': 2, 'left': {'value': 3}},
    }
    self.assertEqual(self._values(tree), [[1], [2], [3]])

  def test_number_of_layers_equals_depth(self):
    tree = {
        'value': 1,
        'left': {'value': 2},
        'right': {'value': 3, 'right': {'value': 4}},
    }
    self.assertEqual(len(get_layers(tree)), 3)

  def test_linked_list_str(self):
    layers = get_layers({'value': 1,
                         'left': {'value': 2},
                         'right': {'value': 3}})
    self.assertEqual(str(layers[1]), '2, 3')


if __name__ == '__main__':
  unittest.main()
