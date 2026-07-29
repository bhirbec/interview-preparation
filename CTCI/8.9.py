# Parens
# Difficulty: medium
# Tags: #recursion #backtracking #string
#
# Implement an algorithm to print all valid (i.e. properly opened and closed)
# combinations of n pairs of parentheses.
#
# Input:  a non-negative integer n, the number of parenthesis pairs.
# Output: a list of every valid string of n opening and n closing parentheses.
#         The number of such strings is the n-th Catalan number
#         C(n) = (2n)! / ((n+1)! * n!).
#
# Approach: build the string slot by slot. At each position we may add an
# opening paren if we have not used all n, and a closing paren if there is an
# unmatched opening paren still available. Recording tracks the counts of opened
# and closed parens to keep every prefix valid.
#
# Examples:
#   gen_parens(0) -> ['']
#   gen_parens(1) -> ['()']
#   gen_parens(2) -> ['(())', '()()']
#   gen_parens(3) -> 5 combinations

import unittest
from math import comb


def gen_parens(n):
  depth = n * 2
  buff = [''] * depth
  result = []

  def f(pos=0, open=0, closed=0):
    if pos == depth:
      result.append(''.join(buff))
      return

    if open < n:
      buff[pos] = '('
      f(pos + 1, open + 1, closed)

    if closed < open:
      buff[pos] = ')'
      f(pos + 1, open, closed + 1)

  f()
  return result


def catalan(n):
  return comb(2 * n, n) // (n + 1)


def is_valid_parens(s):
  balance = 0
  for ch in s:
    balance += 1 if ch == '(' else -1
    if balance < 0:
      return False
  return balance == 0


class TestParens(unittest.TestCase):
  def test_zero_pairs(self):
    self.assertEqual(gen_parens(0), [''])

  def test_one_pair(self):
    self.assertEqual(gen_parens(1), ['()'])

  def test_two_pairs(self):
    self.assertEqual(sorted(gen_parens(2)), ['(())', '()()'])

  def test_three_pairs_full_enumeration(self):
    self.assertEqual(
      sorted(gen_parens(3)),
      ['((()))', '(()())', '(())()', '()(())', '()()()'],
    )

  def test_count_is_catalan(self):
    for n in range(0, 8):
      self.assertEqual(len(gen_parens(n)), catalan(n))

  def test_all_results_distinct_valid_and_correct_length(self):
    for n in range(0, 7):
      result = gen_parens(n)
      self.assertEqual(len(result), len(set(result)))
      for s in result:
        self.assertEqual(len(s), 2 * n)
        self.assertTrue(is_valid_parens(s))


if __name__ == '__main__':
  unittest.main()
