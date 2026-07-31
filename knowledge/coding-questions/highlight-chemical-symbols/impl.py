# Highlight Chemical Symbols
#
# You are given a list of names `names` and a list of `symbols`. For each name,
# find a symbol that occurs in it as a contiguous substring and wrap the first
# occurrence of that symbol in square brackets. If several symbols occur in the
# same name, use the longest one; break ties in favor of the earliest occurrence
# in the name. If no symbol occurs in a name, leave the name unchanged. Matching
# is case-sensitive.
#
# Return the list of transformed names, in the same order as `names`.
#
# Constraints:
#   - 0 <= len(names), len(symbols)
#   - names and symbols contain non-empty strings
#
# Examples:
#   names   = ["Amazon", "Microsoft", "Google"]
#   symbols = ["i", "Am", "cro", "Na", "le", "abc"]
#   -> ["[Am]azon", "Mi[cro]soft", "Goog[le]"]
#   ("Microsoft" matches both "i" and "cro"; the longer "cro" wins.)
#
#   names = ["Boron"], symbols = ["xy"]        -> ["Boron"]   (no match)
#   names = ["aaa"],   symbols = ["a", "aa"]   -> ["[aa]a"]   (longest wins)
#   names = ["abab"],  symbols = ["ab", "ba"]  -> ["[ab]ab"]  (tie length,
#                                                              earliest index)


def highlight_symbols(names, symbols):
  # TODO: implement
  raise NotImplementedError
