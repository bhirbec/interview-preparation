# Valid Braces
#
# You are given a string `s` containing only the bracket characters
# '(', ')', '[', ']', '{' and '}'. Return True if the brackets are balanced:
# every opening bracket is closed by a matching bracket of the same type, and
# brackets are closed in the correct (properly nested) order. Otherwise return
# False. The empty string is considered balanced.
#
# Constraints:
#   - 0 <= len(s)
#   - s contains only the six bracket characters ()[]{}
#
# Examples:
#   "{[]{}[{{{}}}]{{}}}" -> True
#   "()"                 -> True
#   ""                   -> True
#   "(]"                 -> False   (mismatched types)
#   "([)]"               -> False   (wrong nesting order)
#   "((("                -> False   (unclosed openers)
#   ")("                 -> False   (closer before any opener)


def valid_braces(s):
  # TODO: implement
  raise NotImplementedError
