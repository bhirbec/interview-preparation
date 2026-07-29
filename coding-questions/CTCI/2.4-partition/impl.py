# Partition
# Difficulty: medium
# Tags: #linked-list #two-pointers
#
# You are given the head of a singly linked list and a partition value k.
# Rearrange the list so that every node with a value less than k comes before
# every node with a value greater than or equal to k. The partition value k
# itself may appear anywhere in the "greater than or equal" section. Nodes on
# either side of the partition do not need to keep their original relative
# order.
#
# Input: head Node of a singly linked list (each node has `value` and
#        `next_node`), and an integer partition value k.
# Output: the head Node of the rearranged list.
#
# Examples:
#   70 -> 134 -> 3 -> 1 -> 10 -> 9, k=10  =>  9 -> 1 -> 3 -> 70 -> 134 -> 10
#     (all values < 10 precede all values >= 10)
#   1 -> 2 -> 3,                    k=5   =>  all on the "less" side
#   6 -> 7 -> 8,                    k=5   =>  all on the "greater/equal" side
#
# Approach: walk the list once, prepending each node to a `left` list when its
# value < k and to a `right` list otherwise, then splice left in front of right.


class Node:
  def __init__(self, value, next_node=None):
    self.value = value
    self.next_node = next_node


def partition(n, k):
  # TODO: implement
  raise NotImplementedError
