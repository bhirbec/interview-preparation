# Shuffle
# Difficulty: medium
# Tags: #recursion #array #math
#
# Produce a perfectly random shuffle of the deck [1, 2, ..., n], meaning each
# of the n! orderings is equally likely. Return the shuffled list.
#
# Input:  a non-negative integer n (the deck size).
# Output: a list that is a permutation of [1, 2, ..., n] (empty list for n = 0).
#
# Approach: recursively shuffle the first n-1 elements, then append element n
# and swap it into a uniformly random position in [0, n-1]. This is the
# recursive form of the Fisher-Yates shuffle.
#
# Because the result is randomized, the tests below assert invariants (the
# output is a permutation of the input deck of the correct length) rather than
# any fixed ordering.
#
# Examples:
#   shuffle(0) -> []
#   shuffle(1) -> [1]
#   sorted(shuffle(5)) -> [1, 2, 3, 4, 5]


def shuffle(n):
  # TODO: implement
  raise NotImplementedError
