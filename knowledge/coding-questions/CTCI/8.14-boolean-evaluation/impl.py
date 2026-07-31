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


def count_eval(expr, result):
  # TODO: implement
  raise NotImplementedError
