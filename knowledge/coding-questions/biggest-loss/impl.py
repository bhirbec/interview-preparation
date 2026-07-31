# Biggest Loss
#
# Difficulty: easy
# Tags: #array #google
#
# You are given a list `prices` where prices[i] is the value of a stock on day i.
# You make a single trade: buy on one day and sell on a strictly later day.
# Return the largest possible LOSS from such a trade, i.e. the maximum value of
# prices[i] - prices[j] over all pairs i < j. If no trade loses money (prices
# never fall after any earlier day), return 0.
#
# Constraints:
#   - 0 <= len(prices)
#   - values may be any integers
#
# Examples:
#   [23, 24, 27, 532, 14, 12, 17, 121, 24, 1344, 0] -> 1344  (buy 1344, sell 0)
#   [1, 2, 3, 4]                                     -> 0     (only rises)
#   [10, 7, 5, 8, 11, 2, 6]                          -> 9     (buy 11, sell 2)
#   [5]                                              -> 0     (no valid trade)
#
# Approach: single pass tracking the highest price seen so far; for each later
# price the candidate loss is (max_so_far - price). Keep the maximum, floored at 0.


def max_loss(prices):
  # TODO: implement
  raise NotImplementedError
