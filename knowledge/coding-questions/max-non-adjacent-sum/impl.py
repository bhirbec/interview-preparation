# Max Non-Adjacent Sum
# Source: https://www.coursera.org/learn/algorithm-design-analysis-2/supplement/mfwuk/week-3-overview
#
# You are given a list of non-negative integer weights arranged in a row (the
# vertices of a path graph). Choose a subset of positions such that no two
# chosen positions are adjacent, maximizing the total weight. Return that
# maximum total (a maximum-weight independent set of the path).
#
# Constraints:
#   - 0 <= len(weights) <= 10^5
#   - 0 <= weights[i]
#
# Examples:
#   max_non_adjacent_sum([2, 7, 9, 3, 1]) == 12   # 2 + 9 + 1
#   max_non_adjacent_sum([5, 1, 1, 5])    == 10   # 5 + 5 — greedy on big
#                                                 # neighbours fails here
#   max_non_adjacent_sum([4])             == 4
#   max_non_adjacent_sum([])              == 0


def max_non_adjacent_sum(weights):
  # TODO: implement
  raise NotImplementedError
