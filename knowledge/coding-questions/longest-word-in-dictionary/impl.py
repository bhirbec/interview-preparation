# Longest Word in Dictionary
#
# You are given a list of strings `words`. Return the longest word in `words`
# that can be built one character at a time by other words in `words`: every
# proper prefix of the answer must itself appear in `words`.
#
# If several words tie for the maximum length, return the lexicographically
# smallest one. If no word qualifies, return "".
#
# Constraints:
#   - 0 <= len(words) <= 10^4
#   - words consist of lowercase English letters
#   - the list may contain duplicates
#
# Examples:
#   ["w", "wo", "wor", "worl", "world"]  -> "world"
#   ["a", "banana", "app", "appl", "ap", "apply", "apple"]  -> "apple"
#     ("apple" and "apply" both build up from "a"/"ap"/"app"/"appl";
#      "apple" is lexicographically smaller)
#   ["abc", "bc"]       -> ""    ("abc" needs "a" and "ab", "bc" needs "b")
#   ["abc", "bc", "c"]  -> "c"   (a one-character word has no proper prefix to
#                                 check, so it always qualifies)
#   []                  -> ""


def longest_word(words):
  # TODO: implement
  raise NotImplementedError
