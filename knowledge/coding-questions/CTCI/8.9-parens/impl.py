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


def gen_parens(n):
  # TODO: implement
  raise NotImplementedError
