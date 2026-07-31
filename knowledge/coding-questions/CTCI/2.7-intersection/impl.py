# Intersection
#
# You are given the heads of two singly linked lists. Determine whether the two
# lists intersect, and if they do, return the node at which the intersection
# begins. Intersection is defined by reference (identity), not by value: two
# lists intersect when they share a physical node, after which they run through
# the same tail. If the lists do not intersect, return None.
#
# Input: two head Nodes n1 and n2 (each node has `value` and `next_node`).
# Output: the shared intersection Node, or None if the lists are disjoint.
#
# Examples:
#   n1: 70 -> 134 -> 3 -> 1 -> 10 -> 9 -\
#                                        721 -> 12 -> 33   => intersects at 721
#   n2:                     7 -> 11 ----/
#
#   Two fully separate lists                              => None
#   Both heads being the same node                        => that node


class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node


def find_intercept(n1, n2):
  # TODO: implement
  raise NotImplementedError
