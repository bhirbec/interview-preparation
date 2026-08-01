# Check Character Ordering
#
# You are given an input string `text` and an `ordering` string made of distinct
# characters. Return True if, considering only the characters of `text` that also
# appear in `ordering`, they occur in exactly the relative order given by
# `ordering`: every occurrence of ordering[0] must come before every occurrence
# of ordering[1], which must come before every occurrence of ordering[2], and so
# on. Characters of `text` not present in `ordering` are ignored.
#
# Equivalently: keep only the characters of `text` that appear in `ordering`,
# collapse consecutive duplicates, and check the result equals `ordering`.
#
# Constraints:
#   - the characters of `ordering` are distinct
#
# Examples:
#   text = "hello world!", ordering = "hlo!" -> False
#       (the two l's are not all before the o's: ... l l o ... o l ...)
#   text = "hello world!", ordering = "!od"  -> False
#       ('!' appears after o and d, but the ordering wants it first)
#   text = "hello world!", ordering = "he!"  -> True
#   text = "aaaabbbcccc", ordering = "ac"    -> True


def check_ordering(text, ordering):
  # TODO: implement
  raise NotImplementedError
