# Evaluate Reverse Polish Notation
#
# You are given a list of strings `tokens` representing a valid arithmetic
# expression in Reverse Polish (postfix) notation. Each token is either an
# integer (possibly negative) or one of the operators "+", "-", "*", "/".
#
# Evaluate the expression and return the result as an integer. Division between
# two integers truncates toward zero (e.g. 7 / -2 == -3 in normal math rounds
# to -3.5; truncation gives -3). Operands of an operator are the two most
# recently produced values: in "a b -", a is the left operand (a - b).
#
# Constraints:
#   - 1 <= len(tokens) <= 10^4
#   - the expression is valid: operators always have two operands, and there
#     is no division by zero
#
# Examples:
#   ["2", "1", "+", "3", "*"]  -> 9      ((2 + 1) * 3)
#   ["4", "13", "5", "/", "+"] -> 6      (4 + (13 / 5))
#   ["18"]                     -> 18
#   ["7", "-2", "/"]           -> -3     (truncates toward zero)


def eval_rpn(tokens):
  # TODO: implement
  raise NotImplementedError
