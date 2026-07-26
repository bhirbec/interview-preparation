# Boolean Evaluation
# Difficulty: hard
# Tags: #recursion #dynamic-programming
#
# You are given a boolean expression consisting of the symbols 0 (false), 1
# (true), and the operators & (AND), | (OR), and ^ (XOR), and a desired boolean
# result. Return the number of ways of parenthesizing the expression such that it
# evaluates to the desired result.
#
# Input:
#   expr   -- a string with no spaces, e.g. '1^0|0|1'. Operands are single
#             characters '0'/'1'; operators are one of & | ^.
#   result -- the target value, 0 or 1.
# Output:
#   The integer count of full parenthesizations that evaluate to result.
#
# Examples:
#   count_eval('1^0|0|1', 0) -> 2
#   count_eval('0&0&0&1^1|0', 1) -> 10
#   count_eval('1', 1) -> 1
#   count_eval('1', 0) -> 0
#
# Approach: recurse on every operator position, splitting the expression into a
# left and right sub-expression. For each split, combine the counts of the two
# sides across the four (left_result, right_result) pairs that make the operator
# produce the target result. Memoize on (sub-expression, target) to avoid the
# exponential recomputation of overlapping sub-problems.

import unittest

funcs = {
  '^': lambda a, b: int(a) ^ int(b),
  '|': lambda a, b: int(a) or int(b),
  '&': lambda a, b: int(a) and int(b),
}


def count_eval(expr, result):
  memo = {}

  def _count_eval(expr, result):
    if len(expr) == 1:
      return 1 if int(expr) == result else 0

    key = expr, result
    hit = memo.get(key)
    if hit is not None:
      return hit

    s = 0
    for left, op, right in split(expr):
      f = funcs[op]

      for r1, r2 in ((0, 0), (0, 1), (1, 0), (1, 1)):
        if f(r1, r2) == result:
          # NOTE: recurse via _count_eval (not the public count_eval) so the
          # shared memo is actually consulted; the original called count_eval,
          # which allocated a fresh memo on every sub-call and defeated it.
          s += _count_eval(left, r1) * _count_eval(right, r2)

    memo[key] = s
    return s

  return _count_eval(expr, result)


def split(expr):
  n = len(expr)
  for i in range(1, n, 2):
    yield expr[0:i], expr[i], expr[i + 1:]


class TestBooleanEvaluation(unittest.TestCase):
  def test_ctci_examples(self):
    self.assertEqual(count_eval('1^0|0|1', 0), 2)
    self.assertEqual(count_eval('0&0&0&1^1|0', 1), 10)

  def test_single_operand(self):
    self.assertEqual(count_eval('1', 1), 1)
    self.assertEqual(count_eval('1', 0), 0)
    self.assertEqual(count_eval('0', 0), 1)
    self.assertEqual(count_eval('0', 1), 0)

  def test_single_operator(self):
    # '1^0' evaluates to 1 in the only possible parenthesization.
    self.assertEqual(count_eval('1^0', 1), 1)
    self.assertEqual(count_eval('1^0', 0), 0)
    self.assertEqual(count_eval('1&1', 1), 1)
    self.assertEqual(count_eval('1|0', 1), 1)

  def test_counts_are_complementary(self):
    # Total parenthesizations = ways-to-1 + ways-to-0 for any expression.
    expr = '1^0|0|1'
    ways_true = count_eval(expr, 1)
    ways_false = count_eval(expr, 0)
    # Catalan(3) = 5 parenthesizations for 4 operands.
    self.assertEqual(ways_true + ways_false, 5)


if __name__ == '__main__':
  unittest.main()
