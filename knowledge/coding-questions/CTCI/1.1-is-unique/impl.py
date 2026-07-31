# Is Unique
# Difficulty: easy
# Tags: #string #hashtable #bit-manipulation
#
# You are given a string s. Return True if s has all unique characters (no
# character appears more than once), and False otherwise.
#
# Assume the string uses the extended ASCII character set (at most 256 distinct
# code points). An empty string has all unique characters, so it returns True.
#
# Examples:
#   "abcde"  -> True   (every character is distinct)
#   "hello"  -> False  ('l' repeats)
#   ""       -> True   (nothing repeats)
#   "aA"     -> True   (comparison is case-sensitive)
#
# Approach: track which characters have already been seen. unique_char uses a
# boolean lookup table indexed by character code; unique_char_bitvector packs the
# same "seen" flags into a single integer used as a bit vector. If a string is
# longer than the number of possible distinct characters, it cannot be unique.


def unique_char(s):
  # TODO: implement
  raise NotImplementedError
