# Good Numbers
#
# Source: https://www.careercup.com/question?id=5751843230580736
#
# A number t is "good" if it can be written as the sum of two cubes in at least
# two distinct ways, i.e. there exist at least two different unordered pairs of
# positive integers (a, b) with a <= b such that a^3 + b^3 == t. Given n, return
# the sorted list of all good numbers up to and including n.
#
# The smallest good number is 1729 = 1^3 + 12^3 = 9^3 + 10^3 (the Ramanujan /
# taxicab number).
#
# Constraints:
#   - 0 <= n
#   - a and b are positive integers (>= 1)
#
# Examples:
#   n = 1000  -> []                    (no good number that small)
#   n = 1729  -> [1729]
#   n = 4200  -> [1729, 4104]          (4104 = 2^3+16^3 = 9^3+15^3)
#   n = 0     -> []


def good_numbers(n):
  # TODO: implement
  raise NotImplementedError
