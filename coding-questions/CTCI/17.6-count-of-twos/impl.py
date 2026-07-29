# Count of Twos
# Difficulty: hard
# Tags: #math #recursion
#
# Given a non-negative integer n, count the number of digit `2`s that appear
# across all the integers from 0 to n inclusive. Return that count.
#
# Input:  a non-negative integer n.
# Output: the total number of times the digit 2 occurs in 0, 1, ..., n.
#
# Approach: count the 2s contributed at each digit position independently.
# For a position with place value `i` (1, 10, 100, ...), split n into the
# digits above the position (`high`), the digit at the position (`cur`), and
# the digits below (`low`):
#   - cur < 2  -> high * i twos at this position
#   - cur == 2 -> high * i + low + 1 twos
#   - cur > 2  -> (high + 1) * i twos
# Summing over all positions gives the answer in O(number of digits).
#
# NOTE: the original implementation used an incorrect digit decomposition that
# disagreed with brute force for many inputs (e.g. n = 20 gave 12 instead of
# 3). It has been replaced with the per-position count above; `brut_force`
# below is kept as the reference oracle the tests check against.
#
# Examples:
#   count_twos(2)   -> 1   (just "2")
#   count_twos(20)  -> 3   (2, 12, 20)
#   count_twos(25)  -> 9   (2, 12, and 20..25 each contribute a 2, plus 22 twice)
#   count_twos(100) -> 20


def count_twos(n):
  # TODO: implement
  raise NotImplementedError
