# Knapsack
# Source: https://www.coursera.org/learn/algorithm-design-analysis-2/lecture/LIgLJ/the-knapsack-problem
# Source: https://youtu.be/ocZMDMZwhCY?t=2589
#
# You are given a list of items, each a (value, weight) pair of positive
# integers, and a knapsack of integer capacity. Choose a subset of the items
# whose total weight does not exceed the capacity and whose total value is as
# large as possible. Each item can be taken at most once (0/1 knapsack).
# Return that maximum total value.
#
# Constraints:
#   - 0 <= len(items) <= 100
#   - 0 <= capacity <= 10000
#   - values and weights are positive integers
#
# Examples:
#   knapsack([(1, 7), (4, 2), (5, 4), (7, 5)], 9) == 12
#     # take (5,4) and (7,5): weight 9, value 12
#   knapsack([(60, 10), (100, 20), (120, 30)], 50) == 220
#     # greedily taking the densest item first (60/10) is NOT optimal
#   knapsack([], 10) == 0


def knapsack(items, capacity):
  # TODO: implement
  raise NotImplementedError
