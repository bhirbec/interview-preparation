# Divisor-Free Team Size
#
# Difficulty: medium
# Source: https://careercup.com/question?id=5673924747591680
# Tags: #math #twitter
#
# You are given an integer `n`. Players are numbered 1, 2, ..., n. Two players
# conflict when one player's number divides the other's (for example 3 and 9, or
# 2 and 8). A "clean" team is a set of players with no conflicting pair.
#
# Return the smallest team size k such that it is impossible to build a clean team
# of size k -- i.e. every possible team of k players must contain a conflicting
# pair. Equivalently, this is (size of the largest clean team) + 1.
#
# Constraints:
#   - 1 <= n <= 10^6
#
# Examples:
#   n = 10 -> 6   (largest clean team is {6,7,8,9,10}, size 5)
#   n = 1  -> 2   (largest clean team is {1}, size 1)
#   n = 2  -> 2   (1 divides 2, so the largest clean team is size 1)
#   n = 4  -> 3   (largest clean team is {3,4}, size 2)
#
# Approach: the integers in the half-open range (n/2, n] form the largest possible
# clean team (none divides another, since doubling any of them exceeds n), and its
# size is n - n//2; add one to force a conflict.


def divisor_free_team_size(n):
  # TODO: implement
  raise NotImplementedError
