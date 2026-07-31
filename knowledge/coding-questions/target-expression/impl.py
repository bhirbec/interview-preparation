# Target Expression
#
# You are given a list of single digits (each 0-9) and an integer target. Between
# consecutive digits you may insert nothing (concatenating them into a larger
# number), a '+', or a '-'. The digits must be used in their original order, and
# a multi-digit number may not have a leading zero.
#
# Return one expression string (digits with '+'/'-' operators, no spaces) that
# evaluates to target, or None if no such expression exists.
#
# Constraints:
#   - each element of digits is an integer in [0, 9]
#   - the first number in the expression is taken as positive
#   - a number formed from 2+ digits must not start with '0'
#
# Examples:
#   digits = [1, 2, 3, 4], target = 46    -> "12+34"   (12 + 34 = 46)
#   digits = [1, 2, 3, 4], target = 1234  -> "1234"    (concatenate everything)
#   digits = [5],          target = 5     -> "5"
#   digits = [5],          target = 3     -> None
#   digits = [1, 2],       target = 100   -> None


def find_expression(digits, target):
  # TODO: implement
  raise NotImplementedError
