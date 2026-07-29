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

import unittest
import random


def shuffle(n):
  if n == 0:
    return []

  # shuffle 1..n-1
  result = shuffle(n - 1)
  # pick a position between 0 and n-1
  i = int(random.uniform(0, n))
  # append the nth number
  result.append(n)
  # swap the nth element into position i
  result[i], result[n - 1] = result[n - 1], result[i]
  return result


class TestShuffle(unittest.TestCase):
  def test_empty(self):
    self.assertEqual(shuffle(0), [])

  def test_single(self):
    self.assertEqual(shuffle(1), [1])

  def test_is_permutation(self):
    for n in [2, 5, 10, 52]:
      for _ in range(50):
        result = shuffle(n)
        self.assertEqual(len(result), n)
        self.assertEqual(sorted(result), list(range(1, n + 1)))

  def test_no_duplicates(self):
    result = shuffle(52)
    self.assertEqual(len(set(result)), 52)

  def test_covers_multiple_orderings(self):
    # Over many runs the shuffle should not always yield the same ordering.
    seen = {tuple(shuffle(5)) for _ in range(200)}
    self.assertGreater(len(seen), 1)


if __name__ == '__main__':
  unittest.main()
