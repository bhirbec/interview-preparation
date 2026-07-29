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

import unittest

COINS = (25, 10, 5, 1)


def count_repr(n):
  cache = {}

  def f(amount, index):
    if amount == 0:
      return 1
    if index == len(COINS):
      return 0

    key = (amount, index)
    hit = cache.get(key)
    if hit is not None:
      return hit

    coin = COINS[index]
    ways = 0
    qty = 0
    while coin * qty <= amount:
      ways += f(amount - coin * qty, index + 1)
      qty += 1

    cache[key] = ways
    return ways

  return f(n, 0)


class TestCoins(unittest.TestCase):
  def test_zero(self):
    self.assertEqual(count_repr(0), 1)

  def test_penny_only_amounts(self):
    # Amounts below a nickel can only be made with pennies: exactly one way.
    for n in range(1, 5):
      self.assertEqual(count_repr(n), 1)

  def test_small_known_counts(self):
    self.assertEqual(count_repr(5), 2)
    self.assertEqual(count_repr(6), 2)
    self.assertEqual(count_repr(10), 4)

  def test_canonical_quarter(self):
    self.assertEqual(count_repr(25), 13)

  def test_canonical_hundred(self):
    self.assertEqual(count_repr(100), 242)

  def test_matches_brute_force(self):
    # Independent brute-force count of coin multisets summing to n.
    def brute(n):
      count = 0
      for q in range(n // 25 + 1):
        for d in range((n - 25 * q) // 10 + 1):
          for k in range((n - 25 * q - 10 * d) // 5 + 1):
            rem = n - 25 * q - 10 * d - 5 * k
            if rem >= 0:  # remainder is always payable in pennies
              count += 1
      return count

    for n in range(0, 60):
      self.assertEqual(count_repr(n), brute(n))


if __name__ == '__main__':
  unittest.main()
