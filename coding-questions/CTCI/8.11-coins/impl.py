# Coins
# Difficulty: hard
# Tags: #recursion #dynamic-programming
#
# Given an infinite number of quarters (25 cents), dimes (10 cents), nickels
# (5 cents), and pennies (1 cent), write code to calculate the number of ways
# of representing n cents.
#
# Input:  a non-negative integer n, an amount in cents.
# Output: the number of distinct combinations of coins that sum to n. Two
#         representations that use the same multiset of coins count once,
#         regardless of order (so 5 = one nickel = five pennies gives 2 ways,
#         not more).
#
# Approach: consider the coin denominations in a fixed order and, for each
# denomination, try every possible count of that coin before recursing on the
# remaining denominations. Fixing the order prevents counting the same multiset
# of coins as several ordered sequences. Results are memoized on
# (amount, denomination index).
#
# Examples:
#   count_repr(0)   -> 1   (the empty selection)
#   count_repr(5)   -> 2
#   count_repr(10)  -> 4
#   count_repr(25)  -> 13
#   count_repr(100) -> 242
#
# Note: the original implementation summed `f(n - c) + 1` over every coin, which
# both counted ordered sequences (permutations) and over-counted, so it did not
# solve the intended combination-counting problem. It was rewritten to iterate
# denominations in a fixed order, the standard CTCI approach; the tests assert
# the correct combination counts.


def count_repr(n):
  # TODO: implement
  raise NotImplementedError
