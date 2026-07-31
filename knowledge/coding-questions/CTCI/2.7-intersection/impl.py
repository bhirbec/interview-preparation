# Intersection
# Difficulty: medium
# Tags: #linked-list #two-pointers #runner
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
#
# Approach: walk each list to find its tail and length. If the tails are not
# the same object the lists cannot intersect. Otherwise advance a pointer in
# the longer list by the length difference, then advance both pointers in
# lockstep until they reference the same node -- that node is the intersection.


class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node


def find_intercept(n1, n2):
  # TODO: implement
  raise NotImplementedError
