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
# Examples:
#   count_twos(2)   -> 1    (just "2")
#   count_twos(20)  -> 3    (2, 12, 20)
#   count_twos(25)  -> 9    (2, 12, 20, 21, 23, 24, 25 give one 2 each; 22 gives two)
#   count_twos(100) -> 20   (ten 2s in the units place, ten in the tens place)
#
# Approach: count the 2s contributed at each digit position independently.
# For a position with place value `i` (1, 10, 100, ...), split n into the
# digits above the position (`high`), the digit at the position (`cur`), and
# the digits below (`low`):
#   - cur < 2  -> high * i twos at this position
#   - cur == 2 -> high * i + low + 1 twos
#   - cur > 2  -> (high + 1) * i twos
# Summing over all positions gives the answer in O(number of digits).


def count_twos(n):
  # TODO: implement
  raise NotImplementedError
