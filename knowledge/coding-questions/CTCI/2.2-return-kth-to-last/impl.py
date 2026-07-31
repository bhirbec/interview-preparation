# Return Kth to Last
#
# You are given the head of a singly linked list and an integer k (1-indexed).
# Return the value of the kth node counting from the end of the list. k = 1
# refers to the last node. If the list has fewer than k nodes (or is empty),
# return None.
#
# Input: head Node of a singly linked list (each node has `value` and
#        `next_node`), and an integer k >= 1.
# Output: the value stored in the kth-to-last node, or None.
#
# Examples:
#   12 -> 10 -> 3 -> 1 -> 156 -> 43, k=2   =>  156
#   12 -> 10 -> 3 -> 1 -> 156 -> 43, k=1   =>  43
#   1 -> 2 -> 3,                     k=3   =>  1
#   1 -> 2 -> 3,                     k=4   =>  None (k > length)
#   None,                            k=2   =>  None
#
# Two approaches are provided: a runner (two-pointer) version that advances a
# lead pointer k steps ahead then moves both until the lead falls off the end,
# and a recursive version that counts nodes from the tail on the way back up.


class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node


def find_kth_from_tail_runner(n, k):
  # TODO: implement
  raise NotImplementedError
